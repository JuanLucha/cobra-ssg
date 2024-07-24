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
        self.build_dir = os.path.join(self.temp_dir, 'build')
        self.content_sub_dir = os.path.join(self.content_dir, 'subdir')
        os.makedirs(self.content_dir)
        os.makedirs(self.content_sub_dir)
        self.md_file_1 = os.path.join(self.content_dir, 'test_1.md')
        self.md_file_2 = os.path.join(self.content_sub_dir, 'test_2.md')
        with open(self.md_file_1, 'w') as f1:
            f1.writelines([
                "# Title of file 1\n",
                "This is the content of file 1\n"
                "[This is a link to file 2](subdir/test_2)\n"
            ])
        f1.close()
        with open(self.md_file_2, 'w') as f2:
            f2.writelines([
                "# Title of file 2\n",
                "This is the content of file 2\n"
            ])
        f2.close()

    def tearDown(self):
        # Clean the mock content folder
        rmtree(self.temp_dir)

    # Test the whole render process
    def test_cobra_render(self):
        cobra_render(self.content_dir, self.build_dir)

        self.verify_build_dir_created()
        self.verify_folder_tree_copied()
        self.verify_markdown_files_copied_to_build_folder()
        self.verify_markdown_files_converted_to_html()

    # Test the main 'build' folder is created
    def verify_build_dir_created(self):
        self.assertTrue(os.path.exists(self.build_dir), "The build folder wasn't created")

    # Test the whole folder tree is copied from the content folder to the build folder
    def verify_folder_tree_copied(self):
        folders_in_content = get_folder_list(self.content_dir)
        folders_in_build = get_folder_list(self.build_dir)
        for folder in folders_in_content:
            self.assertTrue(folder in folders_in_build, f"Folder {folder} was not created")

    # Test that every markdown file in the content folder is copied to the build folder
    def verify_markdown_files_copied_to_build_folder(self):
        files_in_content = get_file_list(self.content_dir)
        files_in_build = get_file_list(self.build_dir)
        for file in files_in_content:
            file_without_ext = os.path.splitext(file)[0]
            self.assertTrue(file_without_ext in files_in_build, f"File {file_without_ext} was not created")

    # Test that every markdown file is converted into html in the build folder
    def verify_markdown_files_converted_to_html(self):
        files_in_build = get_file_list(self.build_dir)
        for file in files_in_build:
            file_without_ext = os.path.splitext(self.build_dir+file)[0]
            with open(file_without_ext, 'r') as f:
                if file == '/test_1':
                    self.assertEqual(f.read(), """<h1>Title of file 1</h1>
<p>This is the content of file 1
<a href="subdir/test_2">This is a link to file 2</a></p>""")

                if file == '/subdir/test_2':
                    self.assertEqual(f.read(), """<h1>Title of file 2</h1>
<p>This is the content of file 2</p>""")
                    
        
if __name__ == '__main__':
    unittest.main()

