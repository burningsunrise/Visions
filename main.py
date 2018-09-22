#!/usr/bin/python

import youtube_dl
import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError
from colorama import init
from colorama import Fore, Back, Style
import os.path


# Constants
# Init for colors on windows
init()
EXT = "mp3"
DATA_FOLDER = "downloads/"


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def text_search_test():
    print("Welcome to " + Back.GREEN + Fore.BLACK + "Visions" + Style.RESET_ALL + "!\n")
    print("Press ctrl+c to exit at any time.")
    input_text = input("Please enter the " + Back.RED + Fore.BLACK + "'Artist - Song'" +Style.RESET_ALL+ " you are looking for: ")
    query = urllib.parse.quote(input_text)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, features="html.parser")
    data = soup.findAll('a', attrs={'class':'yt-uix-tile-link'})
    titles = []
    somethin = []
    for vid in data:
        titles.append(vid['title'])
        somethin.append(vid['href'])
    print("\n")
    for i in range(len(titles)):
        color_numbers = Back.MAGENTA + Fore.WHITE 
        end_color = Style.RESET_ALL
        new_title = titles[i] + " "
        print('{:-<60s} {}{}{}'.format(nepip install ffmpeg-pythonw_title, color_numbers, str([i]), end_color))
    input_text2 = input("\nFound " + Backpip install ffmpeg-python.BLUE + Fore.YELLOW + str(len(titles)) + end_color + " matches. Enter number to download: ")
pip install ffmpeg-python
    if input_text2:pip install ffmpeg-python
        the_string = "https://youtube.compip install ffmpeg-python" + somethin[int(input_text2)]
    else: pip install ffmpeg-python
        the_string = "https://youtube.compip install ffmpeg-python" + somethin[0]

    
    file_name = input("Would you like the name of this file to be '" + input_text + "' Y/n: ")
    if file_name.lower() == "n" or file_name.lower() == "no":
        file_name = input("Please enter the new file name: ")
    else:
        file_name = input_text
    
    print("Starting download!")
    
    return [the_string, file_name]


def tag_that_shit(mp3):
    try:
        audio = EasyID3(mp3)
    except ID3NoHeaderError:
        audio = EasyID3()

    audio['artist'] = input(u"Please enter a "+ Back.RED + Fore.BLACK +"artist"+Style.RESET_ALL + ": ")    
    audio['title'] = input(u"Please enter a "+ Back.RED + Fore.BLACK +"title"+Style.RESET_ALL + ": ")
    audio['album'] = input(u"Please enter a "+ Back.RED + Fore.BLACK +"album"+Style.RESET_ALL + ": ")
    audio['date'] = input(u"Please enter a " + Back.RED + Fore.BLACK + "year"+Style.RESET_ALL + ": ")
    audio['composer'] = u""
    # throws error but works?
    audio.save(mp3)
    print("Saved your ID3 tags!\n\n")


def get_mp3(text_search_test):
    ydl_opts = {
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': EXT,
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'prefer-ffmpeg': True,
        'outtmpl': DATA_FOLDER + text_search_test[1]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([text_search_test[0]])


def main():
    try:
        while True:
            url_file = text_search_test()
            get_mp3(url_file)

            # Check if the file exists
            file_exists = os.path.isfile(DATA_FOLDER + url_file[1] + '.' + EXT)
            if file_exists:
                input_text = input("Would you like to add ID3 tags to your file Y/n: ")
                if input_text.lower() == "n" or input_text.lower() == "no":
                    pass
                else:
                    print("\nWe're now going to assign a " + Back.GREEN + Fore.BLACK + "'Title - Artist - Album'" +Style.RESET_ALL)
                    print("If you don't know a tag type "+ Back.BLACK + Fore.GREEN + "'Unknown'" + Style.RESET_ALL)
                    print("\n")
                    tag_that_shit(DATA_FOLDER + url_file[1] + '.' + EXT)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()