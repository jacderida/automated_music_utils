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

def get_track_name(track_number, extension):
    if track_number < 10:
        return "0{0} - Track {0}.{1}".format(track_number, extension)
    return "{0} - Track {0}.{1}".format(track_number, extension)

def remove_number_from_duplicate_entry(entry):
    """
    Discogs deals with duplicate artists or labels by appending a number.
    For example, if there are 2 artists named 'Aphex Twin', there will be an
    entry for Aphex Twin and Aphex Twin (2).

    This code detects that and then strips it off.
    """
    match = re.search('.*(\(\d+\))', entry)
    if match:
        entry = entry[0:match.start(1)].strip()
    return entry
