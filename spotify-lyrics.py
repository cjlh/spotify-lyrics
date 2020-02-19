#!/usr/bin/env/python3

""" A Python script that displays the lyrics to the currently playing song on
Spotify in your terminal.

File name: spotify-lyrics.py
Author: Caleb Hamilton
Website: https://github.com/cjlh/spotify-lyrics
License: MIT
Python version: 3

Usage:
    $ python spotify-lyrics.py
"""

import os
import time
import dbus
import requests
from bs4 import BeautifulSoup

old_song_info = None


def get_song_info():
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object(
        "org.mpris.MediaPlayer2.spotify",
        "/org/mpris/MediaPlayer2"
    )

    spotify_metadata = dbus.Interface(
        spotify_bus,
        "org.freedesktop.DBus.Properties"
        ).Get(
            "org.mpris.MediaPlayer2.Player",
            "Metadata"
            )
    return [
        str(spotify_metadata['xesam:artist'][0].title()),
        str(spotify_metadata['xesam:title'])
    ]


def center_string(s):
    terminal_cols = os.popen('tput cols').read()
    return str("{:^" + str(int(terminal_cols) + 10) + "}").format(s)


def print_lyrics(artist, title):
    print(center_string("\n---\n\n"))
    print(center_string("\033[4m" + artist + ": " + title + "\033[0m\n"))

    pageurl = "https://makeitpersonal.co/lyrics?artist=" + artist + \
              "&title=" + title
    lyrics = requests.get(pageurl).text.strip()

    if lyrics == "Sorry, We don't have lyrics for this song yet.":
        wiki_url = "https://lyrics.fandom.com/wiki/"
        title = title.replace(" ", "_")
        artist = artist.replace(" ", "_")
        url = wiki_url + f"{artist}:{title}"

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        lyric_box = str(soup.find("div", {"class": "lyricbox"}))
        lyrics = lyric_box.replace("<br/>", "\n")
        lyrics = lyrics.replace('<div class="lyricbox">', '')
        lyrics = lyrics.replace('<div class="lyricsbreak">', '')
        lyrics = lyrics.replace('</div>', '')

    print(lyrics)


while True:
    song_info = get_song_info()
    if song_info != old_song_info:
        old_song_info = song_info
        os.system('clear')
        print_lyrics(song_info[0], song_info[1])
    time.sleep(1)
