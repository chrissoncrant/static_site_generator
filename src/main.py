from src.dir_management import copy_directory, delete_all_dir_contents
from src.generate_page import generate_page
import os

STATIC_PATH = "./static"
PUBLIC_PATH = "./public"

def main():
    print("Main running...")
    delete_all_dir_contents(PUBLIC_PATH)

    # copy_directory("./content/images", "./static/images")

    copy_directory(STATIC_PATH, PUBLIC_PATH)

    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()