import os

def get_folder_list(path, ignore_folders=[]):
    folders = []
    path_len = len(path)
    for dirpath, dirnames, _ in os.walk(path):
        for dirname in dirnames:
            if dirname in ignore_folders or os.path.basename(dirpath) in ignore_folders:
                continue
            folders.append(os.path.join(dirpath, dirname)[path_len:])
    return folders

def get_file_list(path, ignore_folders=[]):
    files = []
    path_len = len(path)
    for dirpath, _, filenames in os.walk(path):
        if os.path.basename(dirpath) in ignore_folders:
            continue
        for file in filenames:
            files.append(os.path.join(dirpath, file)[path_len:])
    return files
