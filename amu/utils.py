#!/usr/bin/env python
import re
import os
import shutil


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
