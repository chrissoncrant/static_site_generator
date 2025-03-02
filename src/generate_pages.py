import os
import re
from src.md_to_html import extract_title, markdown_to_html_node

def create_rel_path_string(path_of_file, file_name):
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

def replace_image_links(html_string, des_path, folder_name="images"):
    link_pattern = r"\[\? (.*?) \?\]"

    links = re.findall(link_pattern, html_string)

    for link in links:
        file_name = os.path.basename(link)
        image_path = f"{folder_name}/{file_name}"
        correct_path = create_rel_path_string(des_path, image_path)

        pattern_to_replace = f"[? {link} ?]"

        html_string = html_string.replace(pattern_to_replace, correct_path)

    return html_string

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

    styles_link = create_rel_path_string(des_path, "index.css")

    html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string).replace("{{ Styles Link }}", styles_link)

    html_page = replace_image_links(html_page, des_path)
    # print(html_page)

    with open(des_path, "w") as f:
        f.write(html_page)

def generate_pages(source_path, des_path, basepath):
    # print(source_path, des_path)
    source_exists = os.path.exists(source_path)
    if source_exists:
        source_list = os.listdir(source_path)
        # print("source list", source_list)

        for item in source_list:
            # print("##########")
            item_path = os.path.join(source_path, item)
            if os.path.isfile(item_path):
                # print("file")
                # print(item)
                # print(item_path)
                new_des_path = item_path.replace(source_path, des_path).replace('md', 'html')
                # print(new_des_path)
                generate_page(item_path, "template.html", new_des_path, basepath)
            else:
                # print("directory")
                # print(item_path)
                new_des_path = item_path.replace(source_path, des_path)
                # print(new_des_path)
                generate_pages(item_path, new_des_path, basepath)
                # print("###########")
