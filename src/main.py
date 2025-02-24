import os
from src.textnode import TextNode, TextType

SOURCE_PATH = "./static"
PUBLIC_PATH = "./public"

def main():
    print("Main running...")

    source_exists = os.path.exists(SOURCE_PATH)
    public_exists = os.path.exists(PUBLIC_PATH)

    if source_exists and public_exists:
        print("they exist")
        files_in_public = os.listdir(PUBLIC_PATH)

        print(files_in_public)



if __name__ == "__main__":
    main()