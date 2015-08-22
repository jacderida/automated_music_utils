#!/usr/bin/env python
import re
import os
import shutil
import subprocess
from copy import deepcopy
from mutagen.id3 import ID3NoHeaderError
from mock import DEFAULT, Mock
from mutagen.id3 import ID3


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other

def copy_content_to_directory(src, dest):
    for root, directories, files in os.walk(src):
        for directory in directories:
            dir_name = os.path.join(root, directory)
            dest_dir = re.sub(src, dest, dir_name)
            os.mkdir(dest_dir)
        for f in files:
            file_name = os.path.join(root, f)
            dest_file = re.sub(src, dest, file_name)
            shutil.copyfile(file_name, dest_file)

def get_mock_with_stored_call_args(mock):
    new_mock = Mock()
    def side_effect(*args, **kwargs):
        args = deepcopy(args)
        kwargs = deepcopy(kwargs)
        new_mock(*args, **kwargs)
        return DEFAULT
    mock.side_effect = side_effect
    return new_mock

def get_number_of_tracks_on_cd():
    output = subprocess.check_output(['cdparanoia', '-sQ'], stderr=subprocess.STDOUT)
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    track_lines = [m.group(0) for line in lines for m in [re.search('^[0-9].*', line)] if m]
    return len(track_lines)

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
    if tag.has_key('TIT2'):
        tag_data['title'] = tag.getall('TIT2')[0]
    if tag.has_key('TALB'):
        tag_data['album'] = tag.getall('TALB')[0]
    if tag.has_key('TDRC'):
        tag_data['year'] = tag.getall('TDRC')[0]
    if tag.has_key('TRCK'):
        tag_data['trackno'] = tag.getall('TRCK')[0]
    if tag.has_key('TCON'):
        tag_data['genre'] = tag.getall('TCON')[0]
    return tag_data

def get_track_name(track_number, extension):
    if track_number < 10:
        return "0{0} - Track {0}.{1}".format(track_number, extension)
    return "{0} - Track {0}.{1}".format(track_number, extension)
