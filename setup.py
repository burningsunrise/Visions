import ydl_binaries
from shutil import copyfile
import os
import inspect

def setup():
    ydl_binaries.download_ffmpeg("C:\\Users\\Somethin\\Documents\\visions")
    ydl_binaries.update_ydl("C:\\Users\\Somethin\\Documents\\visions")

setup()