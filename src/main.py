from src.dir_management import copy_directory, delete_all_dir_contents
from src.generate_pages import generate_page, generate_pages
from src.paths import STATIC_PATH, PUBLIC_PATH, CONTENT_PATH
import sys

def main():
    print("Main running...")

    print(sys.argv)
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("basepath", basepath)

    delete_all_dir_contents(PUBLIC_PATH)

    # copy_directory("./content/images", "./static/images")

    copy_directory(STATIC_PATH, PUBLIC_PATH)

    generate_pages("content", "docs", basepath)

if __name__ == "__main__":
    main()