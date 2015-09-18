import re
import subprocess
import sys
from contextlib import contextmanager
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

def mp3_has_tags(mp3_source):
    try:
        ID3(mp3_source)
        return True
    except ID3NoHeaderError:
        return False
