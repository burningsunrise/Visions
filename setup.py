#!/usr/bin/python

import ydl_binaries
from shutil import copyfile
import os
import inspect

def setup():
    # Windows users looks like this
    # C:\\Users\\Somethin\\Documents\\visions
    ydl_binaries.download_ffmpeg("/home/somethin/Documents/visions")
    # Leave commented unless you need youtube_dl
    # ydl_binaries.update_ydl("/home/somethin/Documents/visions")

setup()