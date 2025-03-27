import unittest
from nodeoperations import split_nodes_delimiter, split_nodes_image, split_nodes_link
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


if __name__ == "__main__":
    unittest.main()