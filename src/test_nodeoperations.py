import unittest
from nodeoperations import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_text_nodes, markdown_to_blocks
from textnode import TextType, TextNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_delimiter_pair(self):
        """Tests splitting a single pair of delimiters."""
        # Arrange
        node = TextNode("Text with a `code block` here.", TextType.TEXT)
        expected_output = [
            TextNode("Text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" here.", TextType.TEXT),
        ]

        # Act
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        # Assert
        self.assertEqual(result, expected_output)
    
    def test_no_delimiters(self):
        node = TextNode("This is text with no delimiters.", TextType.TEXT)
        expected_output = [TextNode("This is text with no delimiters.", TextType.TEXT)]

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, expected_output)

    def test_two_delimiter_pairs(self):
        node = TextNode("This **text** contains **two** delimiter pairs.", TextType.TEXT)
        expected_output = [TextNode("This ", TextType.TEXT),
                           TextNode("text", TextType.BOLD),
                           TextNode(" contains ", TextType.TEXT),
                           TextNode("two", TextType.BOLD),
                           TextNode(" delimiter pairs.", TextType.TEXT)]
        
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, expected_output)

    def test_two_different_delimiters(self):
        node = [TextNode("This text contains **bold** and `code` delimiters.", TextType.TEXT)]

        nodes_after_bold = split_nodes_delimiter(node, "**", TextType.BOLD)

        expected_after_bold = [TextNode("This text contains ", TextType.TEXT),
                               TextNode("bold", TextType.BOLD),
                               TextNode(" and `code` delimiters.", TextType.TEXT)]
        
        assert nodes_after_bold == expected_after_bold, f"Expected {expected_after_bold}, but got {nodes_after_bold}"

        final_nodes = split_nodes_delimiter(nodes_after_bold, "`", TextType.CODE)

        expected_final_nodes = [TextNode("This text contains ", TextType.TEXT),
                           TextNode("bold", TextType.BOLD),
                           TextNode(" and ", TextType.TEXT),
                           TextNode("code", TextType.CODE),
                           TextNode(" delimiters.", TextType.TEXT)]
        
        assert final_nodes == expected_final_nodes, f"Expected {expected_final_nodes}, but got {final_nodes}"

    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        # It should return the original node if no links are found
        assert new_nodes == [node]


    def test_split_nodes_image_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assert new_nodes == [node]

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to youtube](https://www.youtube.com)", TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes,
        )

    
    def test_split_image_and_link(self):
        node = TextNode(
            "This contains an image ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to github](https://github.com)", TextType.TEXT
            )
        new_nodes = split_nodes_link(split_nodes_image([node]))
        self.assertListEqual(
            [
                TextNode("This contains an image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a link ", TextType.TEXT),
                TextNode("to github", TextType.LINK, "https://github.com"),
            ],
            new_nodes,
        )


    def test_text_to_text_nodes(self):
        self.maxDiff = None
        nodes = [
            TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT),
            TextNode("Here is a **bold** word, an _italic_ one, a `code` block, and an ![image](url) with a [link](url).", TextType.TEXT),
        ]
        result = text_to_text_nodes(nodes)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("Here is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word, an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" one, a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" block, and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(".", TextType.TEXT),
            ], result
        )

    
    def test_markdown_to_blocks(self):
        self.maxDiff = None
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_blanks(self):
        self.maxDiff = None
        md = """
This is a block


with extra blank lines



to see if they are properly removed
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a block",
                "with extra blank lines",
                "to see if they are properly removed"
                ],
        )

    def test_markdown_to_blocks_with_complex_nesting(self):
        md = """
# Heading with **bold**

Paragraph with
multiple lines
and _formatting_

- List item 1
- List item 2

> A blockquote
> with multiple lines

   

Code block:
```python
def hello():
    print("world")
```
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
    "# Heading with **bold**",
    "Paragraph with\nmultiple lines\nand _formatting_",
    "- List item 1\n- List item 2",
    "> A blockquote\n> with multiple lines",
    "Code block:\n```python\ndef hello():\n    print(\"world\")\n```"
],
        )


if __name__ == "__main__":
    unittest.main()