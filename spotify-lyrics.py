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
import argparse
import os
import re
import time
import unicodedata

import dbus
import requests
from bs4 import BeautifulSoup


def get_song_info():
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object(
        "org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2"
    )

    spotify_metadata = dbus.Interface(
        spotify_bus, "org.freedesktop.DBus.Properties"
    ).Get("org.mpris.MediaPlayer2.Player", "Metadata")
    return [
        str(spotify_metadata["xesam:artist"][0]),
        str(spotify_metadata["xesam:title"]),
    ]


def center_string(s):
    terminal_cols = os.popen("tput cols").read()
    return str("{:^" + str(int(terminal_cols) + 10) + "}").format(s)


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def letras_mus_provider(artist, title):
    url = f"https://www.letras.mus.br/{artist}/{title}"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    lyric_box = soup.find("div", {"class": "cnt-letra p402_premium"})

    if not lyric_box:
        return ""

    lyric_box = str(lyric_box)
    lyrics = lyric_box.replace('<div class="cnt-letra p402_premium">', "")
    lyrics = lyrics.replace("</div>", "")
    lyrics = lyrics.replace("<br/>", "\n")
    lyrics = lyrics.replace("</br>", "\n")
    lyrics = lyrics.replace("<br>", "\n")
    lyrics = lyrics.replace("</br>", "\n")
    lyrics = lyrics.replace("</p><p>", "\n\n")
    lyrics = lyrics.replace("</p>", "")
    return lyrics.replace("<p>", "").strip()


def make_it_personal_provider(artist, title):
    pageurl = f"https://makeitpersonal.co/lyrics?artist={artist}&title={title}"
    lyrics = requests.get(pageurl).text.strip()

    if lyrics == "Sorry, We don't have lyrics for this song yet.":
        return ""

    return lyrics


def fandom_provider(artist, title):
    wiki_url = "https://lyrics.fandom.com/wiki/"
    title = title.replace(" ", "_")
    artist = artist.replace(" ", "_")
    url = wiki_url + f"{artist}:{title}"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    lyric_box = soup.find("div", {"class": "lyricbox"})

    if not lyric_box:
        return ""

    lyrics = str(lyric_box).replace("<br/>", "\n")
    lyrics = lyrics.replace('<div class="lyricbox">', "")
    lyrics = lyrics.replace('<div class="lyricsbreak">', "")
    return lyrics.replace("</div>", "")


def format_request_param(request_param):
    request_param = remove_accents(request_param)
    request_param = request_param.replace("&", "e")
    return re.sub("[^A-Za-z0-9\\s]+", "", request_param)


def print_lyrics(artist, title, lyrics_provider_name):
    print(center_string("\n---\n\n"))
    print(center_string("\033[4m" + artist + ": " + title + "\033[0m\n"))

    artist = format_request_param(artist)
    title = format_request_param(title)
    lyrics = ""

    if lyrics_provider_name:
        lyrics_provider = providers[lyrics_provider_name]
        lyrics = lyrics_provider(artist, title)
    else:
        for lyrics_provider in providers.values():
            lyrics = lyrics_provider(artist, title)
            if lyrics:
                break

    print(lyrics or "Lyrics not found")


providers = {
    "make_it_personal": make_it_personal_provider,
    "fandom": fandom_provider,
    "letras_br": letras_mus_provider,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lyrics-provider", help="Lyrics Provider", choices=providers.keys(),
    )
    args = parser.parse_args()

    old_song_info = None
    while True:
        song_info = get_song_info()
        if song_info != old_song_info:
            old_song_info = song_info
            os.system("clear")
            print_lyrics(song_info[0], song_info[1], args.lyrics_provider)
        time.sleep(1)
