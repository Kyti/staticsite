import re

def extract_markdown_images(text):
    img = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return img

def extract_markdown_links(text):
    link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link