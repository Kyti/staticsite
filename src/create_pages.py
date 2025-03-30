import os
from markdowntohtml import markdown_to_html_node
from htmlnode import ParentNode

def extract_title(markdown):
    first_line, content = markdown.split("\n", 1)
    if first_line.lstrip().startswith("#") and not first_line.lstrip().startswith("##"):
        return first_line.lstrip("# ").rstrip(), content
    else:
        raise Exception("No h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    try:
        with open(from_path, 'r') as from_file:
            from_content = from_file.read()
    except FileNotFoundError:
        print(f"Error: The file {from_path} was not found.")
        return
    
    try:
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()
    except FileNotFoundError:
        print(f"Error: The template file {template_path} was not found.")
        return
    
    title, page_content = extract_title(from_content)
    page_node = markdown_to_html_node(page_content)
    page_html = page_node.to_html()
    new_page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", page_html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):

        with open(dest_path, 'w') as dest_file:
            dest_file.write(new_page)

        print(f"Page successfully generated at {dest_path}!")
    
md = """# Heading
Content
"""

result = extract_title(md)

print(result)