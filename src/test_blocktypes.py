import unittest
from blocktypes import BlockType, block_to_block_type

class TestBlockTypes(unittest.TestCase):

    def test_headings(self):
        blocks = [
            "# heading 1",
            "## heading 2",
            "### heading 3",
            "#### heading 4",
            "##### heading 5",
            "###### heading 6",
        ]

        for block in blocks:
            with self.subTest(block=block):
                result = block_to_block_type(block)
                self.assertEqual(result, BlockType.HEAD, f"Failed on: {block}")
    

    def test_code(self):
        block = """```I really hope this code block
        passes the test```"""

        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)


    def test_quote(self):
        block = """>a quote block
>must start with
>this character
>on every line"""

        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)


    def test_ulist(self):
        block = """- this block
- is an unordered list
- and I will be upset if it doesn't return as such"""

        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ULIST)


    def test_olist(self):
        block = """1. this is
2. an ordered list
3. and it better frickin' work"""

        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.OLIST)


    def test_para(self):
        block = """any block that doesn't meet the criteria
        is automatically a regular paragraph block"""

        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARA)


if __name__ == '__main__':
    unittest.main()