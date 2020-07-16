"""Organize music by /Artist/Album/"""

import taglib
from pathlib import Path
import os
import re

# define source and destination
src_base_path = 'D:\\Users\\Mark\\Music\\MusicTools Temp\\'
dest_base_path = 'D:\\Users\\Mark\\Music\\MusicTools\\'

# get all files from source
mp3_paths = list(Path(src_base_path).rglob("*.[mM][pP]3"))
flac_paths = list(Path(src_base_path).rglob("*.[fF][lL][aA][cC]"))
song_paths = mp3_paths + flac_paths

def make_string_windows_compatible(_str):
    _str = re.sub(r'[\/]', '／', _str)
    _str = re.sub(r'[\\]', '＼', _str)
    _str = re.sub(r'[\"]', '＂', _str)
    _str = re.sub(r'[\:]', '：', _str)
    _str = re.sub(r'[\*]', '＊', _str)
    _str = re.sub(r'[\?]', '？', _str)
    _str = re.sub(r'[\<]', '《', _str)
    _str = re.sub(r'[\>]', '》', _str)
    _str = re.sub(r'[\|]', '｜', _str)
    return _str

for song_path in song_paths:
    # get tags info
    tagged_song = taglib.File(str(song_path))
    artist = ",".join(tagged_song.tags["ARTIST"])
    album = tagged_song.tags["ALBUM"][0]
    title = tagged_song.tags["TITLE"][0]
    tagged_song.close()

    # decompose file name
    filename = os.path.basename(song_path)
    extension = filename.split('.')[-1]
    filepath_without_extension = '.'.join(str(song_path).split('.')[0:-1])

    # make string windows compatible
    artist = make_string_windows_compatible(artist)
    album = make_string_windows_compatible(album)
    title = make_string_windows_compatible(title)

    # move music
    if not os.path.exists(dest_base_path + artist + '\\'):
        os.mkdir(dest_base_path + artist + '\\')
    if not os.path.exists(dest_base_path + artist + '\\' + album + '\\'):
        os.mkdir(dest_base_path + artist + '\\' + album + '\\')
    os.rename(str(song_path), (dest_base_path + artist + '\\' + album + '\\' + title + '.' + extension))

    # move lrc
    if os.path.exists(filepath_without_extension + '.lrc'):
        os.rename(filepath_without_extension + '.lrc', (dest_base_path + artist + '\\' + album + '\\' + title + '.' + '.lrc'))
