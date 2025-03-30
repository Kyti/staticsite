from htmlnode import *
from textnode import *
from extractmarkdown import *
from nodeoperations import *
from blocktypes import *
import re

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    final_nodes = []

    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        block_tag, block_children = tag_blocks(block, block_type)

        if block_type == BlockType.CODE:
            code_node = [LeafNode("code", block_children[0])]
            block_node = ParentNode(block_tag, code_node)
            final_nodes.append(block_node)
        elif block_type == BlockType.ULIST or block_type == BlockType.OLIST:
            list_nodes = []
            for child in block_children:
                child_lines = child.splitlines()
                for line in child_lines:
                    line_children = text_to_children(line)
                    html_nodes = [text_node_to_html_node(node) for node in line_children]
                    list_item = ParentNode("li", html_nodes)
                    list_nodes.append(list_item)
                block_node = ParentNode(block_tag, list_nodes)
                final_nodes.append(block_node)
        elif block_type in {BlockType.PARA, BlockType.QUOTE}:
            child_html_nodes = []
            for idx, line in enumerate(block_children[0].splitlines()):
                line_nodes = text_to_children(line)
                child_html_nodes.extend(text_node_to_html_node(n) for n in line_nodes)
                if idx < len(block_children[0].splitlines()) - 1:
                    child_html_nodes.append(LeafNode("br", is_self_closing=True))
            block_node = ParentNode(block_tag, child_html_nodes)
            final_nodes.append(block_node)
        elif block_type == BlockType.HEAD:
            head_children = text_to_children(block_children)
            block_node = ParentNode(block_tag, head_children)
            final_nodes.append(block_node)

    final_html = ParentNode("div", final_nodes)

    return final_html


def tag_blocks(block, block_type):
    if block_type == BlockType.PARA:
        return "p", [block]
    if block_type == BlockType.HEAD:
        h_level = heading_level(block)
        content = block[h_level + 1:].strip()
        return f"h{h_level}", [content]
    if block_type == BlockType.CODE:
        content = block[3:-3]
        return "pre", [content]
    if block_type == BlockType.QUOTE:
        lines = block.splitlines()
        stripped_lines = [line.lstrip('>').rstrip() for line in lines]
        content = '\n'.join(stripped_lines)
        return "blockquote", [content]
    if block_type == BlockType.ULIST:
        return "ul", block.splitlines()
    if block_type == BlockType.OLIST:
        return "ol", block.splitlines()



def heading_level(text):
    match = re.match(r'^(#{1,6})\s', text)
    if match:
        return len(match.group(1))
    return 0


def text_to_children(text):
    child_text_node = TextNode(text, TextType.TEXT)
    children = text_to_text_nodes([child_text_node])
    return children



#with open("src/test_file.md", "r") as f:
#    markdown_content = f.read()
#    html_node = markdown_to_html_node(markdown_content)
#    as_html = html_node.to_html()
#    print(f"As HTML:\n\n {as_html}")
    # then test the result
