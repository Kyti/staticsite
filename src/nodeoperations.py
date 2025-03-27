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
        print(f"remaining_text: {remaining_text}\n")
        markdown_image = extract_markdown_images(remaining_text)
        print(f"markdown_image: {markdown_image}\n")
        sections = []
        image_alt, image_link = "", ""

        if not markdown_image:
            if not remaining_text:
                return
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            print(f"new_nodes no more images: {new_nodes}\n")
            return
       
        for alt, link in markdown_image:
            image_alt, image_link = alt, link
            print(f"image_alt: {image_alt}\nimage_link: {image_link}\n")
            current_section = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            print(f"current_section: {current_section}\n")

            text_type_node = TextNode(current_section[0], TextType.TEXT)
            print(f"text_type_node: {text_type_node}\n")
            new_nodes.append(text_type_node)
            print(f"new_nodes w/text_type_node: {new_nodes}\n")
            image_type_node = TextNode(image_alt, TextType.IMAGE, image_link)
            print(f"image_type_node: {image_type_node}\n")
            new_nodes.append(image_type_node)
            print(f"new_nodes w/image_type_node: {new_nodes}\n")
            sections.append(current_section)
            print(f"sections: {sections}\n")
            remaining_text = ''.join(current_section[2:])
            print(f"remaining_text: {remaining_text}\n")

    
    return new_nodes

def split_nodes_link(old_nodes):
    pass



node = TextNode("This is text with an image ![alt](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT,)
result = extract_markdown_images(node.text)
result2 = split_nodes_image([node])

print(result, result2)