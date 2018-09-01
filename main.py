from __future__ import unicode_literals
import youtube_dl
import ffmpeg
import urllib
import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3


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
    input_text = "Haken - Celestial Elixir"
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
        #print(vid['title'])
        #print('https://youtube.com' + vid['href'])
    #print(len(titles))
    #print(len(somethin))
    #print(titles)
    #print(somethin)
    the_string = "https://youtube.com" + somethin[2]
    return the_string


def tag_that_shit(mp3):
    audio = EasyID3(mp3)
    audio["title"] = u"Celestial Elixir"
    audio['artist'] = u'Haken'
    audio['album'] = u'Aquarius'
    audio['composer'] = u""
    # throws error but works?
    audio.save()


def get_mp3(text_search_test):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'prefer-ffmpeg': True,
        #'ffmpeg_location': os.path.expanduser("/directory/tbd"),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([text_search_test])

#get_mp3(text_search_test())
#tag_that_shit("Celestial Elixir (remastered 2017)-mdh6upXZL6c.mp3")