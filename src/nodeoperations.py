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

        print(f"remaining text: {remaining_text}")
        input("Enter to continue")

        if len(remaining_text) == 0:
            return
        
        markdown_image = extract_markdown_images(remaining_text)

        print(f"markdown_image: {markdown_image}")
        input("Enter to continue")

        if len(markdown_image) == 0:
            text_node = TextNode(remaining_text, TextType.TEXT)
            print(f"text node when no markdown_image: {text_node}")
            new_nodes.append(text_node)
            print(f"new nodes: {new_nodes}")
            input("Enter to continue")
            return

        for alt, link in markdown_image:
            image_alt = alt
            image_link = link

            sections = remaining_text.split(f"![{image_alt}]({image_link})")
            print(f"sections: {sections}")

            text_node = TextNode(sections[0], TextType.TEXT)
            print(f"text node: {text_node}")
            new_nodes.append(text_node)

            image_node = TextNode(image_alt, TextType.IMAGE, image_link)
            print(f"image node: {image_node}")
            new_nodes.append(image_node)

            remaining_text = "".join(sections[1:])
            print(f"remaining text from sections: {remaining_text}")
            input("Enter to continue")

    return new_nodes

def split_nodes_link(old_nodes):
    pass



node = TextNode("This is text with an image ![alt](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT,)
result = split_nodes_image([node])

print(f"1st go:\n{result}")

node = TextNode("", TextType.TEXT,)
result = split_nodes_image([node])

print(f"2nd go:\n{result}")