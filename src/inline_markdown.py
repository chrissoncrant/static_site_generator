from src.textnode import TextNode, TextType
from src.paths import STATIC_PATH, PUBLIC_PATH, CONTENT_PATH
import re
import os

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
   
    allowed_delimiters = ["_", "**", "`"]
    if delimiter not in allowed_delimiters:
        raise ValueError(f"invalid delimiter value: {delimiter}. Only {allowed_delimiters} delimiters can be used")

    match text_type:
        case "bold":
            text_type = TextType.BOLD
        case "italic":
            text_type = TextType.ITALIC
        case "code":
            text_type = TextType.CODE

    delimiter_text_type_correlation = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE
    }

    if text_type != delimiter_text_type_correlation[delimiter]:
        raise ValueError(f"delimiter {delimiter} does not match the text_type {text_type} provided")

    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError("All items in old_node list must be instances of TextNode")

        if node.text_type != TextType.TEXT and node.text_type != "text":
            new_nodes.append(node)
            continue

        delimiter_present = node.text.find(delimiter) != -1
        if not delimiter_present:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)

        for i in range(len(split_text)):
            if i % 2:
                if split_text[i] != "":
                    delimited_node = TextNode(split_text[i], text_type)
                    new_nodes.append(delimited_node)
                    continue
            if split_text[i] != "":        
                text_node = TextNode(split_text[i], TextType.TEXT)
                new_nodes.append(text_node)
    return new_nodes

def find_md_links(text):
    if type(text) != str:
        raise ValueError("argument must be a string")

    md_link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(md_link_pattern, text)

def find_md_images(text):
    if type(text) != str:
        raise ValueError("argument must be a string")
    
    md_image_pattern_with_title = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'

    return re.findall(md_image_pattern_with_title, text)

def split_nodes_images(old_nodes):
    
    new_nodes = []

    for node in old_nodes:

        if not isinstance(node, TextNode):
            raise ValueError(f"Item \"{node}\" must be an instance of TextNode")

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        node_text = node.text
        image_data = find_md_images(node_text)

        if len(image_data) == 0:
            new_nodes.append(TextNode(node_text, TextType.TEXT))
            continue

        for i in range(len(image_data)):
            alt_text = image_data[i][0]
            url = image_data[i][1]

            split = node_text.split(f"![{alt_text}]({url})", 1)

            # Removes titles from images
            if url.find('"') != -1:
                url = url.split(' "')[0]
            
            if url.find("'") != -1:
                url = url.split(" '")[0]

            if split[0] != "":
                text_node = TextNode(split[0], TextType.TEXT)
                new_nodes.append(text_node)

            image_node = TextNode(alt_text, TextType.IMAGE, f"{url}")
            new_nodes.append(image_node)

            if i == len(image_data) - 1:
                if split[1] != "":
                    text_node = TextNode(split[1], TextType.TEXT)
                    new_nodes.append(text_node)
                    continue

            node_text = split[1]           

    return  new_nodes

def split_nodes_links(old_nodes):
    if type(old_nodes) != list:
        raise ValueError("argument must be a list")
    
    if len(old_nodes) == 0:
        raise ValueError("argument is an empty list")
    
    new_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError(f"Item \"{node}\" must be an instance of TextNode")
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        node_text = node.text
        link_data = find_md_links(node_text)

        if len(link_data) == 0:
            new_nodes.append(TextNode(node_text, TextType.TEXT))
            continue
        
        for i in range(len(link_data)):
            link_text = link_data[i][0]
            link_url = link_data[i][1]

            split = node_text.split(f"[{link_text}]({link_url})", 1)

            if split[0] != "":
                text_node = TextNode(split[0], TextType.TEXT)
                new_nodes.append(text_node)

            link_node = TextNode(link_text, TextType.LINK, link_url)
            new_nodes.append(link_node)

            if i == (len(link_data) - 1):
                if split[1] != "":
                    text_node = TextNode(split[1], TextType.TEXT)
                    new_nodes.append(text_node)
                    continue

            node_text = split[1]

    return new_nodes

def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]

    parsed_for_bold = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    parsed_for_italic = split_nodes_delimiter(parsed_for_bold, "_", TextType.ITALIC)
    parsed_for_code = split_nodes_delimiter(parsed_for_italic, "`", TextType.CODE)

    parsed_for_images = split_nodes_images(parsed_for_code)
    parsed_for_links = split_nodes_links(parsed_for_images)
    
    return parsed_for_links