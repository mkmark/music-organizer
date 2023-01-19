# music-organizer
nt command line tool to organize music in format of `{Artist}\{Album}\{Title}.{extension}`

where `{Artist}` is comma splited `ALBUMARTIST` (or when not available, `ARTIST`) 

## Usage
```bat
python music-organizer.py -h
usage: music-organizer.py [-h] -s --src SRC -d --dest DEST

This script organize music from {SRC} to {DEST} in format of {Artist}\{Album}\{Title}.{extension}

optional arguments:
  -h, --help      show this help message and exit
  -s --src SRC    source direcotry path
  -d --dest DEST  destination direcotry path
```

## Example
```bat
python music-organizer.py -s "D:\\Users\\Mark\\Music\\temp\\spotdl\\" -d "D:\\Users\\Mark\\Music\\spotdl\\"
```