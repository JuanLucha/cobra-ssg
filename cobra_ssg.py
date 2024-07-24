import os
from cobra_utils import get_file_list, get_folder_list

def cobra_render(source_folder = 'content', build_folder = 'build'):
    os.mkdir(build_folder)
    folders_to_copy = get_folder_list(source_folder)
    for folder in folders_to_copy:
        os.mkdir(build_folder+folder)

    files_to_copy = get_file_list(source_folder)
    for file in files_to_copy:
        file_without_ext = os.path.splitext(build_folder+file)[0]
        with open(file_without_ext, 'w'):
            pass

