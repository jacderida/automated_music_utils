#!/usr/bin/env python
import re
import os
import shutil
import subprocess
from copy import deepcopy
from tagger import ID3v2
from mock import DEFAULT, Mock


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

    For some unknown reason, the way I'm using the pytagger library causes the null character (x00),
    which is then converted to a string, to be written out to the value of the frame for the tag.
    Until I figure out how to use it properly, I'm just going to leave this as a known issue.
    """
    tag_data = {}
    id3 = ID3v2(path)
    for frame in id3.frames:
        if frame.fid == "TPE1":
            tag_data["artist"] = frame.strings[0].replace('\x00', '')
        elif frame.fid == "TIT2":
            tag_data["title"] = frame.strings[0].replace('\x00', '')
        elif frame.fid == "TALB":
            tag_data["album"] = frame.strings[0].replace('\x00', '')
        elif frame.fid == "TYER":
            tag_data["year"] = frame.strings[0].replace('\x00', '')
        elif frame.fid == "TRCK":
            tag_data["trackno"] = frame.strings[0].replace('\x00', '')
        elif frame.fid == "TCON":
            tag_data["genre"] = frame.strings[0].replace('\x00', '')
    return tag_data
