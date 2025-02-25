import os
from src.md_to_html import extract_title, markdown_to_html_node

def get_css_href(path_of_file, file_name):
        if "/" not in path_of_file:
            return f"./{file_name}"
        
        split = path_of_file.split("/")

        if len(split) == 2:
            return f"./{file_name}"
        
        split.pop(0)
        split.pop(-1)
        nest = ""
        for _ in range(len(split)):
            nest += "../"
        
        return nest + file_name

def generate_page(from_path, template_path, des_path):
    print(f"Generating page from '{from_path}' to '{des_path}' using '{template_path}'")

    content_exists = os.path.exists(from_path)
    if not content_exists:
        raise Exception(f"No source file located at '{from_path}'")
    if not os.path.isfile(from_path):
        raise Exception(f"Source located at '{from_path}' is not a file.")
    with open(from_path) as c:
        content = c.read()
    # print(content)

    template_exists = os.path.exists(template_path)
    if not template_exists:
        raise Exception(f"No template file located at {template_path}")
    if not os.path.isfile(template_path):
        raise Exception(f"Template located at '{template_path}' is not a file.")
    with open(template_path) as t:
        template = t.read()
    # print(template)

    destination_exists = os.path.exists(des_path)
    if not destination_exists:
        dirs_to_create = os.path.dirname(des_path)
        os.makedirs(dirs_to_create, exist_ok=True)

    html_string = markdown_to_html_node(content).to_html()
    # print(html_string)

    title = extract_title(content)
    # print(title)

    styles_link = get_css_href(des_path, "index.css")

    html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string).replace("{{ Styles Link }}", styles_link)
    # print(html_page)

    with open(des_path, "w") as f:
        f.write(html_page)
