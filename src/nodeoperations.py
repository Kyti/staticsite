from textnode import TextType, TextNode

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