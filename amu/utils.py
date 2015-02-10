#!/usr/bin/env python
import re
import os
import shutil
import subprocess
from copy import deepcopy
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

