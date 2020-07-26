# music-organizer
nt command line tool to organize music from <src> to <dest> in format of <Artist>\<Album>\<Title>.<extension>

## Usage
```bat
python music-organizer.py -h
usage: music-organizer.py [-h] -s --src SRC -d --dest DEST

This script organize music from <src> to <dest> in format of <Artist>\<Album>\<Title>.<extension>

optional arguments:
  -h, --help      show this help message and exit
  -s --src SRC    source direcotry path
  -d --dest DEST  destination direcotry path
```

## Example
```bat
python D:\Users\Mark\Documents\Mark\repo\music-organizer\music-organizer.py -s "D:\\Users\\Mark\\Music\\spotdl temp\\" -d "D:\\Users\\Mark\\Music\\spotdl\\"
```