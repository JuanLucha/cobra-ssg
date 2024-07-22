import os

def get_folder_list(path):
    folders = []
    for dirpath, dirnames, _ in os.walk(path):
        for dirname in dirnames:
            folders.append(os.path.join(dirpath, dirname))
    return folders
