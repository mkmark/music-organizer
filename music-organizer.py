"""Organize music from <src> to <dest> in format of <Artist>\\<Album>\\<Title>.<extension>"""

import taglib
from pathlib import Path
import os
import re
import argparse

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

def main():
    # parse args
    parser = argparse.ArgumentParser(description="""
    This script organize music from <src> to <dest> in format of <Artist>\\<Album>\\<Title>.<extension>
    """)
    parser.add_argument("-s --src", \
                        dest = "SRC", \
                        help = "source direcotry path", \
                        required = True)
    parser.add_argument("-d --dest", \
                        dest = "DEST", \
                        help = "destination direcotry path", \
                        required = True)

    # define source and destination
    args = parser.parse_args()
    src_base_path = args.SRC
    dest_base_path = args.DEST

    # get all files from source
    mp3_paths = list(Path(src_base_path).rglob("*.[mM][pP]3"))
    flac_paths = list(Path(src_base_path).rglob("*.[fF][lL][aA][cC]"))
    song_paths = mp3_paths + flac_paths

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

if __name__ == '__main__':
    main()