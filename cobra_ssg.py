import os
import markdown
from cobra_utils import get_file_list, get_folder_list

def cobra_render(source_folder = 'content', build_folder = 'build'):
    # Create the folder structure
    os.mkdir(build_folder)
    folders_to_copy = get_folder_list(source_folder, ['layouts'])
    for folder in folders_to_copy:
        os.mkdir(build_folder+folder)

    # Convert markdown to html and copies the file in the build folder
    files_to_copy = get_file_list(source_folder, ['layouts'])
    for file in files_to_copy:
        html = ''
        with open(source_folder+file, 'r', encoding='utf-8') as f:
            try:
                html = markdown.markdown(f.read())
            except Exception as e:
                print(f"Error converting to html: {str(e)}")

        file_without_ext = os.path.splitext(build_folder+file)[0]
        with open(file_without_ext, 'w', encoding="utf-8", errors="xmlcharrefreplace") as f:
            f.write(html)

