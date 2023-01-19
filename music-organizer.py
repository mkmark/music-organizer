"""Organize music from <src> to <dst> in format of <Artist>\\<Album>\\<Title>.<extension>"""

import taglib
from pathlib import Path
import os
import re
import argparse
import logging


def make_string_windows_compatible(_str):
    _str = re.sub(r"[\/]", "／", _str)
    _str = re.sub(r"[\\]", "＼", _str)
    _str = re.sub(r"[\"]", "＂", _str)
    _str = re.sub(r"[\:]", "：", _str)
    _str = re.sub(r"[\*]", "＊", _str)
    _str = re.sub(r"[\?]", "？", _str)
    _str = re.sub(r"[\<]", "《", _str)
    _str = re.sub(r"[\>]", "》", _str)
    _str = re.sub(r"[\|]", "｜", _str)
    _str = _str.lstrip(" ")
    _str = _str.rstrip(" .")
    return _str


def make_performer_windows_compatible(_str):
    _str = re.sub(r"[\/]", ",", _str)
    _str = re.sub(r"[\\]", ",", _str)
    _str = re.sub(r"[\"]", "＂", _str)
    _str = re.sub(r"[\:]", "：", _str)
    _str = re.sub(r"[\*]", "＊", _str)
    _str = re.sub(r"[\?]", "？", _str)
    _str = re.sub(r"[\<]", "《", _str)
    _str = re.sub(r"[\>]", "》", _str)
    _str = re.sub(r"[\|]", "｜", _str)
    return _str


def main():
    # parse args
    parser = argparse.ArgumentParser(
        description="""
    This script organize music from {SRC} to {DEST} in format of {Artist}\\{Album}\\{Title}.{extension}
    """
    )
    parser.add_argument(
        "-s --src", dest="SRC", help="source direcotry path", required=True
    )
    parser.add_argument(
        "-d --dst", dest="DST", help="destination direcotry path", required=True
    )

    # define source and destination
    args = parser.parse_args()
    src_base_path = args.SRC
    dst_base_path = args.DST

    # get all files from source
    mp3_paths = list(Path(src_base_path).rglob("*.[mM][pP]3"))
    flac_paths = list(Path(src_base_path).rglob("*.[fF][lL][aA][cC]"))
    song_paths = mp3_paths + flac_paths

    for song_path in song_paths:
        # get tags info
        tagged_song = taglib.File(str(song_path))
        try:
            artists = ",".join(tagged_song.tags["ARTIST"])
            album_artists = ",".join(tagged_song.tags["ALBUMARTIST"])
            if album_artists:
                performer = artists
            else:
                performer = album_artists
            album = tagged_song.tags["ALBUM"][0]
            title = tagged_song.tags["TITLE"][0]
        except:
            logging.error("missing info: %s", str(song_path))
            tagged_song.close()
            continue
        tagged_song.close()

        # decompose file name
        filename = os.path.basename(song_path)
        extension = filename.split(".")[-1]
        filepath_without_extension = ".".join(str(song_path).split(".")[0:-1])

        # make string windows compatible
        performer = make_performer_windows_compatible(performer)
        album = make_string_windows_compatible(album)
        title = make_string_windows_compatible(title)

        # move music
        if not os.path.exists(dst_base_path + performer + "\\"):
            os.mkdir(dst_base_path + performer + "\\")
        if not os.path.exists(dst_base_path + performer + "\\" + album + "\\"):
            os.mkdir(dst_base_path + performer + "\\" + album + "\\")
        song_dest_path = (
            dst_base_path + performer + "\\" + album + "\\" + title + "." + extension
        )
        try:
            os.rename(str(song_path), song_dest_path)
            # move lrc
            if os.path.exists(filepath_without_extension + ".lrc"):
                os.rename(
                    filepath_without_extension + ".lrc",
                    (dst_base_path + performer + "\\" + album + "\\" + title + ".lrc"),
                )
        except:
            logging.warning("Files already exists: %s", song_dest_path)
            continue


if __name__ == "__main__":
    main()
