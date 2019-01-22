#!/usr/bin/python3

import argparse
import os
from datetime import datetime
import shutil

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    stat = os.stat(path_to_file)
    try:
        return stat.st_birthtime
    except AttributeError:
        # We're probably on Linux. No easy way to get creation dates here,
        # so we'll settle for when its content was last modified.
        return stat.st_mtime

def unix_to_ts(unixts):
    ts = int(unixts)
    return datetime.utcfromtimestamp(ts)

def ts_to_str(ts):
    return ts.strftime('%Y-%m-%d %H:%M:%S')

def unix_to_str(unixts):
    return ts_to_str(unix_to_ts(unixts))

def handle_photo(path, args, progress = None):
    # file extension from current path
    split = path.split('.')
    ext = split[len(split) - 1] 

    # creation date of the photo
    date = creation_date(path) 
    date = unix_to_ts(date)

    # filename from current path
    filename = '{:02d}{:02d}{:02d}.{}'.format(date.hour, date.minute, date.second, ext)
    bucket_path = '{}/{:04d}/{:02d}/{:02d}'.format(args.device_name, date.year, date.month, date.day)
    file_path = os.path.join(args.output_folder, bucket_path)
    full_path = os.path.join(file_path, filename)

    if not os.path.isfile(full_path):
        # copying and creation of folders
        os.makedirs(file_path, exist_ok=True)
        shutil.copy2(path, full_path)
        print('[{}%] {} -------> {}'.format(progress, path, full_path))
        return full_path

    return None

def handle_path(path, args):
    photos = os.listdir(path)
    nphotos = len(photos)
    print("Found {} files / folders in {}, structuring...".format(nphotos, path))
    for i in range(len(photos)):
        pname = photos[i]
        ppath = os.path.join(path, pname) # full path to photo
        progress = round((i/nphotos)*100)
        if os.path.isfile(ppath):
            newpath = handle_photo(ppath, args, progress=progress) # if path is file
        else:
            handle_path(ppath, args) # if path is folder

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Structure photos to Sun Eye specification')
    parser.add_argument('folders', metavar='FOLDER', type=str, nargs='+')
    parser.add_argument('--output-folder', type=str, default='.')
    parser.add_argument('--device-name', type=str)

    args = parser.parse_args()

    for path in args.folders:
        handle_path(path, args)