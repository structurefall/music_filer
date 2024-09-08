# music_filer
A simple Python program that sorts and extracts downloads from Bandcamp into your music directory.

## Explanation
If you buy a lot of stuff at once from [Bandcamp](https://www.bandcamp.com), which you then download and have to sort into appropriate places on your media server, you may have found that doing so is onerous and frustrating.

This program takes a directory containing files set up in exactly two ways:

* Artist Name - Album Title.zip
* Artist Name - Song Title.mp3

...and creates appropriate artist and title directories in your music library directory, and then extracts/copies the files to appropriate destinations.

Additionally, since artists often change how they format their names over time, the program will search for artist names that look like the one in your file but with different capitalization, and ensure that your existing directory is used.

## Usage

`python music_filer.py -h` to display help

`python music_filer.py -d [path-to-downloads] -l [path-to-music-library]` to run 

Toggles:
`-t` to trust tags instead of filenames. This is particularly useful if you have single unsorted mp3s that belong on an album.

`-c` to strip extraneous copyright text from artists and titles..

## TODO

* Figure out what to do with files that contain ` - ` multiple times
* Support more drastic artist name variations
* Option to strip `(pre-order)` from pre-order albums
* Error handling
* Files should probably be class objects
* Docker, hey why not
* Add fins to lower wind resistance