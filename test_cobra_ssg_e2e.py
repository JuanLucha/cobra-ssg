import unittest
import os
from tempfile import mkdtemp
from shutil import rmtree

from cobra_ssg import cobra_render
from cobra_utils import get_folder_list, get_file_list

class TestCobraRender(unittest.TestCase):
    def setUp(self):
        # Setup the mock content folder
        self.temp_dir = mkdtemp()
        self.content_dir = os.path.join(self.temp_dir, 'content')
        self.pages_dir = os.path.join(self.content_dir, 'pages')
        self.layouts_dir = os.path.join(self.content_dir, 'layouts')
        self.css_dir_source = os.path.join(self.layouts_dir, 'css')
        self.build_dir = os.path.join(self.temp_dir, 'build')
        self.css_dir_target = os.path.join(self.build_dir, 'css')
        self.pages_sub_dir = os.path.join(self.pages_dir, 'subdir')
        os.makedirs(self.content_dir)
        os.makedirs(self.pages_dir)
        os.makedirs(self.layouts_dir)
        os.makedirs(self.css_dir_source)
        os.makedirs(self.pages_sub_dir)
        self.layout_file = os.path.join(self.layouts_dir, 'layout.html')
        self.global_css_file = os.path.join(self.css_dir_source, 'global.css')
        self.layout_css_file_1 = os.path.join(self.css_dir_source, 'test_1.css')
        self.layout_css_file_2 = os.path.join(self.css_dir_source, 'test_2.css')
        self.md_file_1 = os.path.join(self.pages_dir, 'test_1.md')
        self.md_file_2 = os.path.join(self.pages_sub_dir, 'test_2.md')
        with open(self.layout_file, 'w') as f_layout:
            f_layout.writelines([
                "<html>\n",
                "<head></head>\n",
                "<body>\n",
                "<cobra_ssg_content>\n",
                "</body>\n",
                "</html>\n",
            ])
        with open(self.global_css_file, 'w') as f_global_css:
            f_global_css.writelines([
                "* {\n",
                "  margin:0;\n",
                "  padding:0;\n",
                "}\n",
            ])
        with open(self.layout_css_file_1, 'w') as f_layout_css_1:
            f_layout_css_1.writelines([
                "* {\n",
                "  margin:0;\n",
                "  padding:0;\n",
                "}\n",
            ])
        with open(self.layout_css_file_2, 'w') as f_layout_css_2:
            f_layout_css_2.writelines([
                "* {\n",
                "  margin:0;\n",
                "  padding:0;\n",
                "}\n",
            ])
        with open(self.md_file_1, 'w') as f1:
            f1.writelines([
                "# Title of file 1\n",
                "This is the content of file 1\n"
                "[This is a link to file 2](subdir/test_2)\n"
            ])
        with open(self.md_file_2, 'w') as f2:
            f2.writelines([
                "# Title of file 2\n",
                "This is the content of file 2\n"
            ])

        # render the build folder
        cobra_render(self.content_dir, self.build_dir)

    # Test the main 'build' folder is created
    def test_verify_build_dir_created(self):
        self.assertTrue(os.path.exists(self.build_dir), "The build folder wasn't created")

    # Test the whole folder tree is copied from the content folder to the build folder, ignoring layouts folder
    def test_verify_folder_tree_copied(self):
        folders_in_content = get_folder_list(self.content_dir)
        folders_in_build = get_folder_list(self.build_dir)
        for folder in folders_in_content:
            # The /layouts/css folder is copied to /css
            if folder == '/layouts/css':
                folder = '/css'
            if folder == '/layouts':
                self.assertFalse(folder in folders_in_build, f"Folder {folder} was created, but it shouldn't")
            else:
                self.assertTrue(folder in folders_in_build, f"Folder {folder} was not created")

    # Test that every markdown file in the content folder is copied to the build folder
    def test_verify_markdown_files_copied_to_build_folder(self):
        files_in_content = get_file_list(self.content_dir, ['layouts'])
        files_in_build = get_file_list(self.build_dir)
        if len(files_in_build) == 0:
            self.fail("There is no files in the build folder!")
        for file in files_in_content:
            file_name, file_extension = os.path.splitext(file)
            if file_extension == ".css":
                file_to_check = file.replace('/layouts/css', '/css')
            else:
                file_to_check = file_name
            self.assertTrue(file_to_check in files_in_build, f"File {file_to_check} was not created")

    # Test that every markdown file is converted into html with layout in the build folder
    def test_verify_markdown_files_converted_to_html(self):
        files_in_build = get_file_list(self.build_dir, ignore_folders=["css"])
        if len(files_in_build) == 0:
            self.fail("There is no files in the build folder!")
        for file in files_in_build:
            file_without_ext = os.path.splitext(self.build_dir+file)[0]
            with open(file_without_ext, 'r') as f:
                if file == '/pages/test_1':
                    self.assertEqual(f.read(), """<html>
<head>
<link rel="stylesheet" href="../css/global.css">
</head>
<body>
<h1>Title of file 1</h1>
<p>This is the content of file 1
<a href="subdir/test_2">This is a link to file 2</a></p>
</body>
</html>
""")

                elif file == '/pages/subdir/test_2':
                    self.assertEqual(f.read(), """<html>
<head>
<link rel="stylesheet" href="../../css/global.css">
</head>
<body>
<h1>Title of file 2</h1>
<p>This is the content of file 2</p>
</body>
</html>
""")
                else:
                    self.fail(f"The file is not covered by test cases: {file}")

    def tearDown(self):
        # Clean the mock content folder
        rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()

