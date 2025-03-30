import unittest
from create_pages import extract_title

class TestCreatePages(unittest.TestCase):
    def test_extract_title(self):
        md = """# This is the title
        and some content"""

        result = extract_title(md)

        self.assertEqual(result, "This is the title")
    
    def test_extract_title_error(self):
        md = """## This is an incorrect heading
        and some content"""

        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()