import os
import shutil


from newcode import extract_title
from markdown_block import markdown_to_html_node



def recursive_funcion_to_copy(source_directory, destination_directory):
    print(f"Copying contents from {source_directory} to {destination_directory}")

    try:
        dir_contents = os.listdir(source_directory)
    except FileNotFoundError:
        print(f"Error: Source directory not found at {source_directory}")
        return

    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)

    for item_name in dir_contents:
        source_item_path = os.path.join(source_directory, item_name)
        dest_item_path = os.path.join(destination_directory, item_name)

        if os.path.isfile(source_item_path):
            print(f"  Copying file: {source_item_path} to {dest_item_path}")
            shutil.copy(source_item_path, dest_item_path)

        elif os.path.isdir(source_item_path):
            print(f"  Creating directory: {dest_item_path}")
            recursive_funcion_to_copy(source_item_path, dest_item_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.exists(from_path):
        print(f"Error: Markdown file not found at {from_path}")
        return

    if not os.path.exists(template_path):
        print(f"Error: Template file not found at {template_path}")
        return

    try:
        with open(from_path, 'r') as f:
            markdown_content = f.read()
    except Exception as e:
        print(f"Error reading markdown file {from_path}: {e}")
        return

    try:
        with open(template_path, 'r') as f:
            template_content = f.read()
    except Exception as e:
        print(f"Error reading template file {template_path}: {e}")
        return

    try:
        html_content = markdown_to_html_node(markdown_content).to_html()
    except ValueError as e:
        print(f"Error converting markdown to HTML for {from_path}: {e}")
        return

    try:
        page_title = extract_title(markdown_content)
    except ValueError as e:
        print(f"Error extracting title from {from_path}: {e}")
        return

    final_html = template_content.replace("{{ Title }}", page_title).replace("{{ Content }}", html_content)

    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')


    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    try:
        with open(dest_path, 'w') as f:
            f.write(final_html)
    except Exception as e:
        print(f"Error writing final HTML file to {dest_path}: {e}")
        return

    
def generate_pages_recursive(current_content_path, template_path, current_dest_path, basepath):
    print(f"Processing directory: {current_content_path}")

    if not os.path.exists(current_content_path):
        print(f"Error: Content directory not found at {current_content_path}")
        return

    dir_contents = os.listdir(current_content_path)

    os.makedirs(current_dest_path, exist_ok=True)

    for item_name in dir_contents:
        src_item_path = os.path.join(current_content_path, item_name)
        dest_item_path_base = os.path.join(current_dest_path, item_name)

        if os.path.isfile(src_item_path):
            if item_name.endswith(".md"):
                dest_html_path = dest_item_path_base[:-3] + ".html"
                generate_page(src_item_path, template_path, dest_html_path, basepath)

        elif os.path.isdir(src_item_path):
            generate_pages_recursive(src_item_path, template_path, dest_item_path_base, basepath)