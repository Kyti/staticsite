from textnode import TextType, TextNode
from extractmarkdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        if delimiter not in remaining_text:
            new_nodes.append(old_node)
            continue

        while delimiter in remaining_text:
            first_pos = remaining_text.find(delimiter)
            second_pos = remaining_text.find(delimiter, first_pos + len(delimiter))

            if second_pos == -1:
                raise Exception("Invalid markdown: missing closing delimiter")
                
            if first_pos > 0:
                new_nodes.append(TextNode(remaining_text[:first_pos], TextType.TEXT))

                text_between = remaining_text[first_pos + len(delimiter):second_pos]
                new_nodes.append(TextNode(text_between, text_type))

                remaining_text = remaining_text[second_pos + len(delimiter):]

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text


        if len(remaining_text) == 0:
            continue
        
        markdown_image = extract_markdown_images(remaining_text)

        for alt, link in markdown_image:
            image_alt = alt
            image_link = link

            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            text_node = TextNode(sections[0], TextType.TEXT)
            new_nodes.append(text_node)
            image_node = TextNode(image_alt, TextType.IMAGE, image_link)
            new_nodes.append(image_node)

            remaining_text = "".join(sections[1:])

        if remaining_text:
            text_node = TextNode(remaining_text, TextType.TEXT)
            new_nodes.append(text_node)


    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text


        if len(remaining_text) == 0:
            continue
        
        markdown_link = extract_markdown_links(remaining_text)

        for text, url in markdown_link:
            link_text = text
            link_url = url

            sections = remaining_text.split(f"[{link_text}]({link_url})", 1)
            text_node = TextNode(sections[0], TextType.TEXT)
            new_nodes.append(text_node)
            link_node = TextNode(link_text, TextType.LINK, link_url)
            new_nodes.append(link_node)

            remaining_text = "".join(sections[1:])

        if remaining_text:
            text_node = TextNode(remaining_text, TextType.TEXT)
            new_nodes.append(text_node)


    return new_nodes


def text_to_text_nodes(old_nodes):
    nodes_after_images = split_nodes_image(old_nodes)
    current_nodes = split_nodes_link(nodes_after_images)
    # print(f"current nodes before delimiters:\n{current_nodes}\n")
    
    delimiters = [
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE),
    ]

    for delimiter, text_type in delimiters:
        current_nodes = split_nodes_delimiter(current_nodes, delimiter, text_type)
        # print(f"delimiter: {delimiter}, current nodes after checking delimiter: {current_nodes}\n")


    return current_nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []

    for block in blocks:
        stripped = block.strip()
        if len(stripped) > 0:
            stripped_blocks.append(stripped)
        else:
            continue


    return stripped_blocks