import os
import math

def convert_size(size : int):
    '''
    Converts a size in bytes to a human readable format
    '''
    units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
    i = math.floor(math.log(size, 1024)) if size > 0 else 0
    size = round(size / 1024 ** i, 2)

    return f"{size} {units[i]}"

def get_files_size(file_paths: list):
    '''
    Returns the size of a list of files in a human readable format
    '''
    total_size = sum([os.path.getsize(path) for path in file_paths])
    return convert_size(total_size)