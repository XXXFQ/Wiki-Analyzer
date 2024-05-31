import os
import math

def convert_bytes_to_string(size : int) -> str:
    '''
    Converts a size in bytes to a human readable format
    
    Parameters:
    size : int
        Size in bytes
    
    Returns:
    str
        Human readable size
    '''
    units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
    i = math.floor(math.log(size, 1024)) if size > 0 else 0
    size = round(size / 1024 ** i, 2)

    return f"{size} {units[i]}"

def sum_files_size(file_paths: list) -> str:
    '''
    Returns the size of a list of files in a human readable format
    
    Parameters:
    file_paths : list
        List of file paths
    
    Returns:
    str
        Human readable size
    '''
    total_size = sum([os.path.getsize(path) for path in file_paths])
    return convert_bytes_to_string(total_size)