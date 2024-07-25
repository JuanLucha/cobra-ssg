import os
import markdown
from cobra_utils import get_file_list, get_folder_list

def cobra_render(source_folder = 'content', build_folder = 'build'):
    layouts_folder = 'layouts'
    layouts_full_path = os.path.join(source_folder, layouts_folder)
    content_tag = '<cobra_ssg_content>'

    # Create the folder structure
    os.mkdir(build_folder)
    folders_to_copy = get_folder_list(source_folder, [layouts_folder])
    for folder in folders_to_copy:
        os.mkdir(build_folder+folder)

    # Load layouts
    layouts = []
    layouts_to_load = get_file_list(layouts_full_path)
    for layout in layouts_to_load:
        with open(layouts_full_path+layout, 'r', encoding='utf-8') as layout_content:
            layouts.append({'name': layout, 'content': layout_content.read()})

    # Convert markdown to html and copies the file in the build folder
    files_to_copy = get_file_list(source_folder, [layouts_folder])
    for file in files_to_copy:
        html_file_content = ''
        with open(source_folder+file, 'r', encoding='utf-8') as f:
            try:
                html_page_content = markdown.markdown(f.read())
                html_file_content = layouts[0]['content'].replace(content_tag, html_page_content)
            except Exception as e:
                print(f"Error converting to html: {str(e)}")

        file_without_ext = os.path.splitext(build_folder+file)[0]
        with open(file_without_ext, 'w', encoding="utf-8", errors="xmlcharrefreplace") as f:
            f.write(html_file_content)

