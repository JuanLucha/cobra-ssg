import unittest
import os
from tempfile import mkdtemp
from shutil import rmtree

from cobra_ssg import cobra_render
from cobra_ssg.cobra_utils import get_folder_list, get_file_list

class TestCobraRender(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Setup the mock content folder
        self.temp_dir = mkdtemp()
        self.content_dir = os.path.join(self.temp_dir, 'content')
        self.pages_dir = os.path.join(self.content_dir, 'pages')
        self.layouts_dir = os.path.join(self.content_dir, 'layouts')
        self.css_dir_source = os.path.join(self.layouts_dir, 'css')
        self.js_dir = os.path.join(self.layouts_dir, 'js')
        self.build_dir = os.path.join(self.temp_dir, 'build')
        self.css_dir_target = os.path.join(self.build_dir, 'css')
        self.pages_sub_dir = os.path.join(self.pages_dir, 'subdir')
        self.blocks_dir = os.path.join(self.layouts_dir, 'blocks')
        os.makedirs(self.content_dir)
        os.makedirs(self.pages_dir)
        os.makedirs(self.layouts_dir)
        os.makedirs(self.css_dir_source)
        os.makedirs(self.pages_sub_dir)
        os.makedirs(self.blocks_dir)
        os.makedirs(self.js_dir)
        self.layout_file_1 = os.path.join(self.layouts_dir, 'default.html')
        self.layout_file_2 = os.path.join(self.layouts_dir, 'layout_alternative.html')
        self.global_css_file = os.path.join(self.css_dir_source, 'global.css')
        self.layout_css_file_1 = os.path.join(self.css_dir_source, 'test_1.css')
        self.layout_css_file_2 = os.path.join(self.css_dir_source, 'test_2.css')
        self.md_file_1 = os.path.join(self.pages_dir, 'test_1.md')
        self.md_file_2 = os.path.join(self.pages_sub_dir, 'test_2.md')
        self.menu_block_file = os.path.join(self.blocks_dir, 'menu_block.html')
        self.js_file = os.path.join(self.js_dir, 'global.js')
        with open(self.layout_file_1, 'w') as f_layout:
            f_layout.writelines([
                "<html>\n",
                "<head>\n"
                "<title>Title of the default layout</title>"
                "</head>\n",
                "<body>\n",
                "<block_menu_block>\n",
                "<cobra_ssg_content>\n",
                "</body>\n",
                "</html>\n",
            ])
        f_layout.close()
        with open(self.layout_file_2, 'w') as f_layout:
            f_layout.writelines([
                "<html>\n",
                "<head>\n"
                "<title>Title of the layout alternative</title>"
                "</head>\n",
                "<body>\n",
                "<block_menu_block>\n",
                "<cobra_ssg_content>\n",
                "</body>\n",
                "</html>\n",
            ])
        f_layout.close()
        with open(self.global_css_file, 'w') as f_global_css:
            f_global_css.writelines([
                "* {\n",
                "  margin:0;\n",
                "  padding:0;\n",
                "}\n",
            ])
        f_global_css.close()
        with open(self.layout_css_file_1, 'w') as f_layout_css_1:
            f_layout_css_1.writelines([
                "* {\n",
                "  margin:0;\n",
                "  padding:0;\n",
                "}\n",
            ])
        f_layout_css_1.close()
        with open(self.layout_css_file_2, 'w') as f_layout_css_2:
            f_layout_css_2.writelines([
                "* {\n",
                "  margin:0;\n",
                "  padding:0;\n",
                "}\n",
            ])
        f_layout_css_2.close()
        with open(self.md_file_1, 'w') as f1:
            f1.writelines([
                "# Title of file 1\n",
                "This is the content of file 1\n"
                "[This is a link to file 2](subdir/test_2)\n"
            ])
        f1.close()
        with open(self.md_file_2, 'w') as f2:
            f2.writelines([
                "---\n",
                "layout: layout_alternative\n"
                "---\n",
                "# Title of file 2\n",
                "This is the content of file 2\n"
            ])
        f2.close()
        with open(self.menu_block_file, 'w') as f_block:
            f_block.writelines([
                "<nav>\n",
                "<ul>\n",
                "<li><a href=\"/section1\">Section 1</a></li>\n",
                "<li><a href=\"/section2\">Section 2</a></li>\n",
                "<li><a href=\"/section3\">Section 3</a></li>\n",
                "<li><a href=\"/section4\">Section 4</a></li>\n",
                "</ul>\n",
                "</nav>\n",
            ])
        f_block.close()
        with open(self.js_file, 'w') as f_js:
            f_js.writelines([
                "console.log(1+1)\n",
            ])
        f_js.close()

        # render the build folder
        cobra_render(self.content_dir, self.build_dir)
        
        # read the built content files
        file_without_ext = os.path.splitext(self.build_dir+'/pages/test_1')[0]
        with open(file_without_ext, 'r') as f:
            self.file1_content = f.read()
        f.close()
        file_without_ext = os.path.splitext(self.build_dir+'/pages/subdir/test_2')[0]
        with open(file_without_ext, 'r') as f:
            self.file2_content = f.read()
        f.close()

    # Test the main 'build' folder is created
    def test_verify_build_dir_created(self):
        self.assertTrue(os.path.exists(self.build_dir), "The build folder wasn't created")

    # Test the whole folder tree is copied from the content folder to the build folder, ignoring layouts folder
    def test_verify_folder_tree_copied(self):
        folders_in_content = get_folder_list(self.content_dir)
        folders_in_build = get_folder_list(self.build_dir)
        for folder in folders_in_content:
            if folder == '/layouts/blocks':
                continue
            elif folder == '/layouts/css':        # The /layouts/css folder is copied to /css
                folder = '/css'
            elif folder == '/layouts/js':         # The /layouts/js folder is copied to /js
                folder = '/js'
            elif folder == '/layouts':
                self.assertFalse(folder in folders_in_build, f"Folder {folder} was created, but it shouldn't")
            else:
                self.assertTrue(folder in folders_in_build, f"Folder {folder} was not created")

    # Test that every markdown file in the content folder is copied to the build folder
    def test_verify_markdown_files_copied_to_build_folder(self):
        files_in_content = get_file_list(self.content_dir, ['layouts', 'blocks'])
        files_in_build = get_file_list(self.build_dir)
        if len(files_in_build) == 0:
            self.fail("There is no files in the build folder!")
        for file in files_in_content:
            file_name, file_extension = os.path.splitext(file)
            if file_extension == ".css":
                file_to_check = file.replace('/layouts/css', '/css')
            elif file_extension == ".js":
                file_to_check = file.replace('/layouts/js', '/js')
            else:
                file_to_check = file_name
            self.assertTrue(file_to_check in files_in_build, f"File {file_to_check} was not created")

    # Test that every markdown file is converted into html with layout in the build folder
    def test_markdown_files_converted_to_html(self):
        self.assertIn("""
<h1>Title of file 1</h1>
<p>This is the content of file 1
<a href="subdir/test_2">This is a link to file 2</a></p>
""", self.file1_content)

        self.assertIn("""
<h1>Title of file 2</h1>
<p>This is the content of file 2</p>
""", self.file2_content)

    # Test that every converted file includes the global css file
    def test_global_css_is_included(self):
        self.assertIn("""
<link rel="stylesheet" href="../css/global.css">
""", self.file1_content)

        self.assertIn("""
<link rel="stylesheet" href="../../css/global.css">
""", self.file2_content)

    # Test that every converted file includes the global js file
    def test_global_js_is_included(self):
        self.assertIn("""
<script src="../js/global.js" defer></script>
</head>
""", self.file1_content)

        self.assertIn("""
<script src="../../js/global.js" defer></script>
</head>
""", self.file2_content)

    # Test that the menu block is included in the layout
    def test_menu_block_is_included(self):
        for file in [self.file1_content, self.file2_content]:
            self.assertIn("""
<body>
<nav>
<ul>
<li><a href="/section1">Section 1</a></li>
<li><a href="/section2">Section 2</a></li>
<li><a href="/section3">Section 3</a></li>
<li><a href="/section4">Section 4</a></li>
</ul>
</nav>
""", file)

    # Test that the right layout is used in rendering each markdown file
    def test_the_right_layout_is_used(self):
        self.assertIn("<title>Title of the default layout</title>", self.file1_content)
        self.assertIn("<title>Title of the layout alternative</title>", self.file2_content)

    @classmethod
    def tearDownClass(self):
        # Clean the mock content folder
        rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
