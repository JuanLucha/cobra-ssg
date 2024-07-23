import os

def get_folder_list(path):
    folders = []
    path_len = len(path)
    for dirpath, dirnames, _ in os.walk(path):
        for dirname in dirnames:
            folders.append(os.path.join(dirpath, dirname)[path_len:])
    return folders
