from src.dir_management import copy_directory, delete_all_dir_contents
from src.generate_pages import generate_page
from src.paths import STATIC_PATH, PUBLIC_PATH, CONTENT_PATH

def main():
    print("Main running...")
    delete_all_dir_contents(PUBLIC_PATH)

    # copy_directory("./content/images", "./static/images")

    copy_directory(STATIC_PATH, PUBLIC_PATH)

    generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")

if __name__ == "__main__":
    main()