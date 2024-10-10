import os
import markdown
import frontmatter
import shutil
from cobra_utils import get_file_list, get_folder_list

def cobra_render(source_folder = 'content', build_folder = 'build'):
    layouts_folder = 'layouts'
    css_folder_source = f"{source_folder}/{layouts_folder}/css"
    css_folder_target = f"{build_folder}/css"
    layouts_full_path = os.path.join(source_folder, layouts_folder)
    menus_full_path = os.path.join(layouts_full_path, 'menus')
    content_tag = '<cobra_ssg_content>'

    # Create the folder structure
    os.mkdir(build_folder)
    folders_to_copy = get_folder_list(path=source_folder, ignore_folders=[layouts_folder])
    for folder in folders_to_copy:
        os.mkdir(build_folder+folder)

    # Copy the css files
    shutil.copytree(css_folder_source, css_folder_target)

    # Load layouts
    layouts = []
    layouts_to_load = [layout for layout in get_file_list(path=layouts_full_path, ignore_folders=["menus"]) if os.path.splitext(layout)[1] != '.css']
    if not len(layouts_to_load):
        raise Exception(f"No layouts found in {layouts_full_path}")
    for layout in layouts_to_load:
        with open(layouts_full_path+layout, 'r', encoding='utf-8') as layout_content:
            name = os.path.splitext(layout)[0].lstrip('/')
            layouts.append({'name': name, 'content': layout_content.read()})

    # Load menus
    menus = []
    menus_to_load = [menu for menu in get_file_list(path=menus_full_path)]
    for menu in menus_to_load:
        with open(menus_full_path+menu, 'r', encoding='utf-8') as menu_content:
            tag = f"<menu_{os.path.splitext(menu)[0].lstrip('/')}>"
            menus.append({'tag': tag, 'content': menu_content.read()})

    # insert the menus into the layouts
    for layout in layouts:
        for menu in menus:
            if menu["tag"] in layout["content"]:
                layout["content"] = layout["content"].replace(menu["tag"], menu["content"])

    # Convert markdown to html and copies the file in the build folder
    content_files_to_copy = get_file_list(path=source_folder, ignore_folders=[layouts_folder, "css", "menus"])
    if not len(content_files_to_copy):
        raise Exception(f"No files found in {source_folder}")
    for file in content_files_to_copy:
        html_file_content = ''
        backtracks = max(file.count("/") - 1, 0)
        global_css_string = f"<link rel=\"stylesheet\" href=\"{backtracks*'../'}css/global.css\">"
        with open(source_folder+file, 'r', encoding='utf-8') as f:
            try:
                file_content_raw = f.read()
                page_frontmatter, file_content = frontmatter.parse(file_content_raw)
                layout_name = page_frontmatter.get("layout", "default")
                layout = next((layout for layout in layouts if layout["name"] == layout_name), None)
                html_page_content = markdown.markdown(file_content)
                html_file_content = layout['content'].replace(content_tag, html_page_content)
                # Insert global css path
                if "</head>" in html_file_content:
                    html_file_content = html_file_content.replace('</head>', f'\n{global_css_string}\n</head>')
            except Exception as e:
                print(f"Error converting to html: {str(e)}")

        file_without_ext = os.path.splitext(build_folder+file)[0]
        with open(file_without_ext, 'w', encoding="utf-8", errors="xmlcharrefreplace") as f:
            f.write(html_file_content)

