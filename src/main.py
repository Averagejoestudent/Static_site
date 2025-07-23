import sys
from page_creator import recursive_funcion_to_copy,generate_pages_recursive
import os
import shutil
import sys






def main():
    print("Starting STATIC STIE GENERATOR")
    
    source_directory="static"
    destination_directory = "docs"
    content_path = "content"
    template_path = "template.html"

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        if not basepath.endswith('/'):
             basepath += '/'

    
    if not os.path.exists(source_directory):
        print(f"Error: Static directory not found at {source_directory}")
        sys.exit(1)

    if os.path.exists(destination_directory):
        print(f"Cleaning destination directory: {destination_directory}")
        shutil.rmtree(destination_directory)
    
    print(f"Creating destination directory: {destination_directory}")
    os.mkdir(destination_directory)
    
    recursive_funcion_to_copy(source_directory,destination_directory)
    generate_pages_recursive(content_path, template_path, destination_directory, basepath)

    print("Static site generation finished.")
    
if __name__ == "__main__":
    main()