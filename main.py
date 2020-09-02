#!/usr/bin/env python3
import urllib.parse
import os.path
import youtube_dl
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from colorama import init, Fore, Back, Style
import requests


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


def text_search():
    print("Welcome to " + Back.GREEN + Fore.BLACK + "Visions" + Style.RESET_ALL + "!\n")
    print("Press ctrl+c to exit at any time.")
    input_text = input("Please enter the 'Artist - Song' you are looking for: ")
    url = requests.get("https://www.youtube.com/results?search_query="+ urllib.parse.quote(input_text, safe=""))
    url = url.text[url.text.index("ytInitialData")+17::]
    url = url[:url.index('window["ytInitialPlayerResponse"]')-6]
    true = True; false = False
    url = eval(url)
    lotsOfShits = url["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
    results = {}
    for miniShits in lotsOfShits:
        if "itemSectionRenderer" not in miniShits.keys():
            continue
        for content in miniShits["itemSectionRenderer"]["contents"]:
            try:
                if "videoRenderer" in content.keys():
                    results[content["videoRenderer"]["title"]["runs"][0]["text"]] = content["videoRenderer"]["videoId"]
            except Exception as e:
                print(e)
    i = 0
    for title, video_id in results.items():
        color_numbers = Back.MAGENTA + Fore.WHITE 
        end_color = Style.RESET_ALL
        new_title = title + " "
        print('{:-<60s} {}{}{}'.format(new_title, color_numbers, str([i]), end_color))
        i+=1
    input_text2 = input("\nFound " + str(len(results)) + " matches. Enter number to download: ")

    if input_text2:
        the_string = "https://www.youtube.com/watch?v=" + list(results.values())[int(input_text2)]
    else:
        the_string = "https://www.youtube.com/watch?v=" + list(results.values())[0]

    
    file_name = input("\nWould you like the name of this file to be '" + input_text + "' Y/n: ")
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

    audio['artist'] = input(u"Please enter a artist: ")    
    audio['title'] = input(u"Please enter a title: ")
    audio['album'] = input(u"Please enter a album: ")
    audio['date'] = input(u"Please enter a year: ")
    audio['composer'] = u""
    # throws error but works?
    audio.save(mp3)
    print("Saved your ID3 tags!\n\n")


def get_mp3(text_search):
    ydl_opts = {
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': EXT,
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'prefer-ffmpeg': True,
        'outtmpl': DATA_FOLDER + text_search[1],
        'ffmpeg_location': os.getcwd()
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([text_search[0]])


def main():
    try:
        while True:
            url_file = text_search()
            get_mp3(url_file)

            # Check if the file exists
            file_exists = os.path.isfile(DATA_FOLDER + url_file[1] + '.' + EXT)
            if file_exists:
                input_text = input("\nWould you like to add ID3 tags to your file Y/n: ")
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