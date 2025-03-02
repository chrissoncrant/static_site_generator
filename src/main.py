from src.dir_management import copy_directory, delete_all_dir_contents
from src.generate_pages import generate_pages
from src.paths import STATIC_PATH, PUBLIC_PATH, DOCS_PATH
import sys

def main():
    print("Main running...")

    print(sys.argv)
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("basepath", basepath)

    if basepath == "/":
        destination_path = PUBLIC_PATH
    else:
        destination_path = DOCS_PATH

    delete_all_dir_contents(destination_path)

    # copy_directory("./content/images", "./static/images")

    copy_directory(STATIC_PATH, destination_path)

    if destination_path == PUBLIC_PATH:
        des = "public"
    else:
        des = "docs"

    generate_pages("content", des, basepath)

if __name__ == "__main__":
    main()