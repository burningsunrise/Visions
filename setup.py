#!/usr/bin/env python3
import os
import ydl_binaries

def setup():
    ydl_binaries.download_ffmpeg(os.getcwd())

if __name__ == "__main__":
    setup()
