import os
from markdowntohtml import markdown_to_html_node
import time

def extract_title(markdown):
    first_line = markdown.split("\n", 1)[0]
    if first_line.lstrip().startswith("#") and not first_line.lstrip().startswith("##"):
        return first_line.lstrip("# ").rstrip()
    else:
        raise Exception("No h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    try:
        start_time = time.time()
        with open(from_path, 'r') as from_file:
            from_content = from_file.read()
        print(f"Read {from_path} successfully. Time taken: {time.time() - start_time:.2f}s")
    except Exception as e:
        print(f"Error reading {from_path}: {e}")
        return
    
    try:
        start_time = time.time()
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()
        print(f"Read {template_path} successfully. Time taken: {time.time() - start_time:.2f}s")
    except Exception as e:
        print(f"Error reading {template_path}: {e}")
        return
    
    try:
        start_time = time.time()
        title = extract_title(from_content)
        print(f"Extracted title: {title}. Time taken: {time.time() - start_time:.2f}s")
    except Exception as e:
        print(f"Error extracting title: {e}")
        return

    try:
        start_time = time.time()
        print(f"Converting the following markdown to HTML:\n{from_content[:100]}...")
        page_node = markdown_to_html_node(from_content)
        page_html = page_node.to_html()
        print(f"Converted markdown to HTML. Time taken: {time.time() - start_time:.2f}s")
    except Exception as e:
        print(f"Error converting markdown to HTML: {e}")
        return
    
    try:
        start_time = time.time()
        new_page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", page_html)
        print(f"Replaced placeholders in template. Time taken: {time.time() - start_time:.2f}s")
    except Exception as e:
        print(f"Error replacing placeholders: {e}")
        return
    
    try:
        start_time = time.time()
        dest_dir = os.path.dirname(dest_path)
        print(f"Checking if the destination directory {dest_dir} exists...")
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            print(f"Created directories for {dest_path}. Time taken: {time.time() - start_time:.2f}s")
        else:
            print(f"Destination directory {dest_dir} already exists.")
    except Exception as e:
        print(f"Error creating directories: {e}")
        return

    try:
        start_time = time.time()
        with open(dest_path, 'w') as dest_file:
            dest_file.write(new_page)
        print(f"Successfully wrote to {dest_path}.  Time taken: {time.time() - start_time:.2f}s")
    except Exception as e:
        print(f"Error writing to {dest_path}: {e}")
        return

    print(f"Page successfully generated at {dest_path}!")

def generate_multiple_pages(content_dir, template_path, public_dir):
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, content_dir)
                dest_path = os.path.join(public_dir, relative_path.replace('.md', '.html'))

                dest_dir = os.path.dirname(dest_path)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                generate_page(from_path, template_path, dest_path)
                print(f"Generated page for {relative_path}")