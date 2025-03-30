from textnode import *
import os
import shutil
import logging
from create_pages import generate_page

    
def copy_static_to_public(source_dir, dest_dir):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    source_dir = os.path.abspath(source_dir)
    dest_dir = os.path.abspath(dest_dir)

    logging.info(f"Source directory: {source_dir}")
    logging.info(f"Destination directory: {dest_dir}")

    if not os.path.exists(source_dir):
        logging.error(f"Source directory does not exist: {source_dir}")
        return

    if os.path.exists(dest_dir):
        for filename in os.listdir(dest_dir):
            file_path = os.path.join(dest_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    logging.debug(f"Deleted file: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    logging.debug(f"Deleted directory: {file_path}")
            except Exception as e:
                logging.error(f"Failed to delete {file_path}. Reason: {e}")
    else:
        os.makedirs(dest_dir)
        logging.debug(f"Created destination directory: {dest_dir}")

    def recursive_copy(src, dst):
        logging.debug(f"Copying from {src} to {dst}")
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s_item = os.path.join(src, item)
            d_item = os.path.join(dst, item)
            if os.path.isdir(s_item):
                recursive_copy(s_item, d_item)
            elif os.path.isfile(s_item):
                try:
                    shutil.copy2(s_item, d_item)
                    logging.debug(f"Copied file: {s_item} -> {d_item}")
                except Exception as e:
                    logging.error(f"Failed to copy {s_item} to {d_item}. Reason: {e}")

    recursive_copy(source_dir, dest_dir)

def main():
    source_dir = "static"
    destination_dir = "public"

    copy_static_to_public(source_dir, destination_dir)
    print(f"Static content copied from {source_dir} to {destination_dir}.")
    
    from_path = "content/index.md"
    template_path = "template.html"
    dest_path = "public/index.html"

    generate_page(from_path, template_path, dest_path)



if __name__ == "__main__":
    main()