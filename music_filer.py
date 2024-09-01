#!/usr/bin/python3

from os import listdir, path, makedirs
from re import sub
from shutil import copyfile
from sys import argv
from zipfile import ZipFile

import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel('INFO')

SOURCE_DIR = argv[1]
MUSIC_DIR = 'SETME'
ARTIST_DIR_LIST = listdir(MUSIC_DIR)
ARTIST_DIR_LIST_LOWERED = [artist.lower() for artist in ARTIST_DIR_LIST]

def process_file(filename):
    logger.info('Now processing %s', filename)
    if filename.endswith('.zip'):
        filetype = 'zip'
    elif filename.endswith('.mp3'):
        filetype = 'mp3'
    else:
        logger.warn('Invalid file: %s', filename)
        return False
    artist = sub(r' - .*', str(), filename)
    title = sub(r'.* - (.*)\.(zip|mp3)', r'\1', filename)
    logger.info('Artist is %s, title is %s', artist, title)
    artist_directory = get_artist_directory(artist)

    full_path = path.join(MUSIC_DIR, artist_directory, title)
    logger.info('Full path is %s, creating now...', full_path)
    makedirs(full_path, exist_ok=True)

    if filetype == 'zip':
        logger.info('Extracting %s to %s', filename, full_path)
        with ZipFile(path.join(SOURCE_DIR, filename)) as compressed_file:
            compressed_file.extractall(path=full_path)
    elif filetype == 'mp3':
        logger.info('Copying %s to %s', filename, full_path)
        copyfile(path.join(SOURCE_DIR, filename), path.join(full_path, filename))

def get_artist_directory(artist):
    artist_dir = None
    if artist.lower() in ARTIST_DIR_LIST_LOWERED:
        logger.info('Existing artist directory found for %s', artist)
        for directory in ARTIST_DIR_LIST:
            if directory.lower() == artist.lower():
                artist_dir = directory
                break
        if artist_dir is None:
            logger.error('We should have found a directory for %s but we didn\'t', artist)
            return False
    else:
        artist_dir = artist
    return artist_dir

def main():
    logger.info('Getting files from %s', SOURCE_DIR)
    file_list = listdir(SOURCE_DIR)
    for file in file_list:
        process_file(file)
    logger.info('Complete!')



if __name__ == '__main__':
    main()