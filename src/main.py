import os
from src.dir_management import copy_from_static_to_public, delete_all_dir_contents

STATIC_PATH = "./static"
PUBLIC_PATH = "./public"

def main():
    print("Main running...")
    delete_all_dir_contents(PUBLIC_PATH)
    copy_from_static_to_public(STATIC_PATH, PUBLIC_PATH)


if __name__ == "__main__":
    main()