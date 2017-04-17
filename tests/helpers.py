import re
import subprocess
import sys
from contextlib import contextmanager
from subprocess import check_output
from mutagen.flac import FLAC
from mutagen.id3 import APIC, ID3, ID3NoHeaderError
from StringIO import StringIO


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

def get_mp3_artwork_data(mp3_source):
    subprocess_args = ['mid3v2', '--list', mp3_source]
    result = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE)
    output = [x for x in result.stdout.readlines() if "APIC" in x][0]
    match = re.search('\(([^)]+)\)', output)
    splits = match.groups(0)[0].split(',')
    size_string = splits[1].strip()
    return (splits[0].strip(), int(size_string[0:size_string.index(' ')]))

def get_flac_artwork_data(flac_source):
    output = check_output(['metaflac', '--list', '--block-type=PICTURE', flac_source])
    length = _get_metaflac_attribute_value(output, 'length')
    image_type = _get_metaflac_attribute_value(output, 'MIME type')
    return (image_type, int(length))

def mp3_has_tags(mp3_source):
    try:
        ID3(mp3_source)
        return True
    except ID3NoHeaderError:
        return False

def flac_has_tags(flac_source):
    tag = FLAC(flac_source)
    return len(tag.keys()) > 0

def get_id3_tag_data(path):
    """
    Gets the ID3 tag from an MP3.

    It's possible for this code to deal with MP3s that have no tags, which is the reason
    for the exception handling.
    """
    tag_data = {}
    try:
        tag = ID3(path)
    except ID3NoHeaderError:
        return tag_data
    if tag.has_key('TPE1'):
        tag_data['artist'] = tag.getall('TPE1')[0]
    if tag.has_key('TPE2'):
        tag_data['album_artist'] = tag.getall('TPE2')[0]
    if tag.has_key('TIT2'):
        tag_data['title'] = tag.getall('TIT2')[0]
    if tag.has_key('TALB'):
        tag_data['album'] = tag.getall('TALB')[0]
    if tag.has_key('TDRC'):
        tag_data['year'] = tag.getall('TDRC')[0]
    if tag.has_key('TRCK'):
        tag_data['trackno'] = tag.getall('TRCK')[0]
    if tag.has_key('TPOS'):
        tag_data['discno'] = tag.getall('TPOS')[0]
    if tag.has_key('TCON'):
        tag_data['genre'] = tag.getall('TCON')[0]
    if tag.has_key('COMM:comm:eng'):
        tag_data['comment'] = tag.getall('COMM')[0]
    if tag.has_key('APIC'):
        tag_data['artwork'] = True
    else:
        tag_data['artwork'] = False
    return tag_data

def get_flac_tag_data(path):
    """
    Gets the vorbis comment tag data from a FLAC.

    It's possible for this code to deal with FLACs that have no tags, which is the reason
    for the exception handling.
    """
    tag_data = {}
    tag = FLAC(path)
    if tag.has_key('ARTIST'):
        tag_data['artist'] = tag['ARTIST'][0]
    if tag.has_key('ALBUMARTIST'):
        tag_data['album_artist'] = tag['ALBUMARTIST'][0]
    if tag.has_key('TITLE'):
        tag_data['title'] = tag['TITLE'][0]
    if tag.has_key('ALBUM'):
        tag_data['album'] = tag['ALBUM'][0]
    if tag.has_key('DATE'):
        tag_data['year'] = tag['DATE'][0]
    if tag.has_key('GENRE'):
        tag_data['genre'] = tag['GENRE'][0]
    if tag.has_key('DESCRIPTION'):
        tag_data['comment'] = tag['DESCRIPTION'][0]
    if tag.has_key('TRACKNUMBER'):
        tag_data['trackno'] = tag['TRACKNUMBER'][0]
    if tag.has_key('DISCNUMBER'):
        tag_data['discno'] = tag['DISCNUMBER'][0]
    return tag_data

def _get_metaflac_attribute_value(metaflac_output, attribute):
    index = metaflac_output.rfind(attribute + ':')
    line = metaflac_output[index:metaflac_output.find('\n', index)]
    return line.split(':')[1].strip()
