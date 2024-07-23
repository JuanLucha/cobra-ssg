import unittest
import os
from tempfile import mkdtemp
from shutil import rmtree

from cobra_ssg import cobra_render
from cobra_utils import get_folder_list

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
                "# Title of file 1",
                "This is the content of file 1"
                "[This is a link to file 2](subdir/test_2)"
            ])
        f1.close()
        with open(self.md_file_2, 'w') as f2:
            f2.writelines([
                "# Title of file 2",
                "This is the content of file 2"
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

    # Test the main 'build' folder is created
    def verify_build_dir_created(self):
        self.assertTrue(os.path.exists(self.build_dir), "The build folder wasn't created")

    # Test the whole folder tree is copied from the content folder to the build folder
    def verify_folder_tree_copied(self):
        folders_in_content = get_folder_list(self.content_dir)
        folders_in_build = get_folder_list(self.build_dir)
        for folder in folders_in_content:
            self.assertTrue(folder in folders_in_build, f"Folder {folder} was not created")
        
if __name__ == '__main__':
    unittest.main()

