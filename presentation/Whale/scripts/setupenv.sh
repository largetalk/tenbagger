#!/bin/bash
sudo easy_install pip
pip install virtualenvwrapper

source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv whale
workon whale
pip install -r requirements.txt
