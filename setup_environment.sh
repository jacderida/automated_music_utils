#!/usr/bin/env bash

present_path=$(pwd)

[[ -d "$present_path/env" ]] && rm -rf env
virtualenv env
source env/bin/activate
if [[ -z "$HTTP_PROXY" ]]; then
    pip install -r requirements.txt
else
    pip install -r requirements.txt --proxy=$HTTP_PROXY
fi
export PYTHONPATH=$present_path # For use with pylint.

if [[ ! -e "tests/integration/data/song.mp3" ]]; then
    mkdir tests/integration/data
    cd tests/integration/data
    curl -O http://jacderida-misc.s3.amazonaws.com/song.mp3
    cd $present_path
fi
