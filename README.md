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
First, change the `MUSIC_DIR` variable in the file to the full path of your library.
Then:

    python music_filer.py <directory of your files>

## TODO

* Figure out what to do with files that contain ` - ` multiple times
* Support more drastic artist name variations
