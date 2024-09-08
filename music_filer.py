#!/usr/bin/python3

from argparse import ArgumentParser
from os import getcwd, listdir, path, makedirs
from re import sub
from shutil import copyfile, rmtree
from sys import argv
from uuid import uuid1
from zipfile import ZipFile

from mutagen import File as Mp3File

import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel('INFO')

SOURCE_DIR = str()
MUSIC_DIR = str()
ARTIST_DIR_LIST = list()
ARTIST_DIR_LIST_LOWERED = list()
BY_TAGS = False
TEMPDIR = str()

COPYRIGHT_SYMBOLS = [
    '©',
    '™',
    '®'
]

def init_args():
    parser = ArgumentParser(
        prog='Music_Filer',
        description='Sorts your Music Downloads'
    )
    parser.add_argument(
        '--downloads', '-d', 
        help="Path to directory containing the downloads / .zip files (SOURCE)",
        required=True
    )
    parser.add_argument(
        '--library', '-l',
        help="Path to the top level folder of your music library (DESTINATION)",
        required=True
    )
    parser.add_argument(
        '--by-tags', '-t',
        help="Use ID3 tags instead of filenames",
        required=False,
        action='store_true'
    )
    parser.add_argument(
        '--copyright-trim', '-c',
        help="Trim trailing copyrights in titles and artist names",
        required=False,
        action='store_true'
    )
    args = parser.parse_args()
    return args

def _process_mp3_by_tags(filename, directory):
    '''Check mp3 tags for artist and title. If no album, use the track name.'''
    logger.info("ASDFASDFASDF %s", SOURCE_DIR)
    mp3 = Mp3File(path.join(directory, filename))
    artist = mp3.tags['TPE1'].text[0]
    if 'TALB' in mp3.tags.keys():
        title = mp3.tags['TALB'].text[0]
    else:
        title = mp3.tags['TIT2'].text[0]
    return (artist, title)

def _extract_tempfile(filename):
    '''Get a single mp3 file out of a zip for tag analysis'''
    tempfile_name = str()
    with ZipFile(path.join(SOURCE_DIR, filename)) as compressed_file:
        for file in compressed_file.namelist():
            if file.endswith('.mp3'):
                tempfile_name = file
                break
        logger.info('Extracting %s to %s', tempfile_name, TEMPDIR)
        compressed_file.extract(tempfile_name, path=TEMPDIR)
        return tempfile_name

def process_by_tags(filename, filetype):
    '''Get artist and title by mp3 tag instead of filename'''
    if filetype == 'mp3':
        result = _process_mp3_by_tags(filename, SOURCE_DIR)
    elif filetype == 'zip':
        single_track = _extract_tempfile(filename)
        result = _process_mp3_by_tags(single_track, TEMPDIR)
    return result

def copyright_trim(artist, title):
    '''Look for a copyright symbol and assume that all text after that is junk'''
    for symbol in COPYRIGHT_SYMBOLS:
        if symbol in artist or symbol in title:
            artist = sub(fr' *{symbol}.*', str(), artist)
            title = sub(fr' *{symbol}.*', str(), title)
            break
    return artist, title

def process_file(filename):
    '''Process an individual mp3 or zip file'''
    logger.info('Now processing %s', filename)
    if filename.endswith('.zip'):
        filetype = 'zip'
    elif filename.endswith('.mp3'):
        filetype = 'mp3'
    else:
        logger.warn('Invalid file: %s', filename)
        return False

    if BY_TAGS:
        artist, title = process_by_tags(filename, filetype)
    else:
        artist = sub(r' - .*', str(), filename)
        title = sub(r'.* - (.*)\.(zip|mp3)', r'\1', filename)

    if COPYRIGHT_TRIM:
        artist, title = copyright_trim(artist, title)

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
    '''Check existing artist directories for a directory with different capitalization,
    and prefer that capitalization if found'''
    artist_dir = None
    print(type(artist))
    print(artist)
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
    if BY_TAGS:
        logger.info('Creating temporary directory %s', TEMPDIR)
        makedirs(TEMPDIR)
    for file in file_list:
        process_file(file)
    if TEMPDIR:
        logger.info('Removing temporary directory %s and all temp files', TEMPDIR)
        rmtree(TEMPDIR)
    logger.info('Complete!')


if __name__ == '__main__':
    args = init_args()
    SOURCE_DIR = args.downloads
    MUSIC_DIR = args.library
    ARTIST_DIR_LIST = listdir(MUSIC_DIR)
    ARTIST_DIR_LIST_LOWERED = [artist.lower() for artist in ARTIST_DIR_LIST]
    BY_TAGS = args.by_tags
    if BY_TAGS:
        TEMPDIR = path.join(getcwd(), 'mfilertemp-' + str(uuid1()))
    COPYRIGHT_TRIM = args.copyright_trim

    main()