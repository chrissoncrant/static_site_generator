from src.htmlnode import HTMLNode, ParentNode, LeafNode
from src.textnode import TextNode, text_node_to_html_node
from src.block_markdown import markdown_to_blocks, block_to_block_type
from src.inline_markdown import text_to_textnodes

#############################
# GENERAL HELPER FUNCTIONS
#############################
def string_list_to_text_nodes(string_list):
    if type(string_list) != list:
        raise TypeError(f"Argument is of type '{type(string_list).__name__}', but must be a list.")
    node_list = []
    for string in string_list:
        string_text_nodes = text_to_textnodes(string)
        node_list.append(string_text_nodes)
    return node_list

def text_nodes_to_leaf_nodes(nodes):
    if type(nodes) != list:
        raise TypeError(f"Argument is of type '{type(nodes).__name__}', but must be a list.")
    node_list = []
    for node in nodes:
        if not isinstance(node, TextNode):
            raise ValueError("Argument's items must be instances of TextNodes")
        html_node = text_node_to_html_node(node)
        node_list.append(html_node)
    return node_list

#############################
# CODE FUNCTIONS
#############################
def code_to_html(code):
    code = code.strip("```").strip()
    text_nodes = text_to_textnodes(code)
    leaf_nodes = text_nodes_to_leaf_nodes(text_nodes)
    pre_node = ParentNode("pre", leaf_nodes)
    code_node = ParentNode("code", [pre_node])
    return code_node

#############################
# LIST FUNCTIONS
#############################
def extract_list_text(block):
    list_items = []

    split_at_newline = block.split("\n")

    for line in split_at_newline:
        text = line.split(" ", 1)[1]
        list_items.append(text)
    
    return list_items

def list_to_html(list_string):
    list_strings = extract_list_text(list_string)

    strings_text_nodes = string_list_to_text_nodes(list_strings)

    leaf_nodes = []
    for text_nodes in strings_text_nodes:
        string_leafs = text_nodes_to_leaf_nodes(text_nodes)
        leaf_nodes.append(string_leafs)

    li_nodes = []
    for leaf_list in leaf_nodes:
        parent_node = ParentNode("li", leaf_list)
        li_nodes.append(parent_node)

    return li_nodes

#############################
# HEADER FUNCTION
#############################
def heading_to_html(heading_block):
    heading_type, text_value = heading_block.split(" ", 1)
    heading_tag = f"h{len(heading_type)}"
    text_nodes = text_to_textnodes(text_value)
    leaf_nodes = text_nodes_to_leaf_nodes(text_nodes)
    parent_node = ParentNode(heading_tag, leaf_nodes)
    return parent_node

#############################
# QUOTE FUNCTION
#############################
def extract_quote(quote_block):
    split = quote_block.split(">")
    def strip_leading_space(lines):
        new_list = []
        
        for line in lines:
            if line == "":
                continue
            if line.startswith(" "):
                stripped = line.lstrip()
                new_list.append(stripped)
            else:
                new_list.append(line)

        return new_list
    
    cleaned = strip_leading_space(split)
    return "".join(cleaned)

def quote_to_html(quote_block):
    extracted = extract_quote(quote_block)
    text_nodes = text_to_textnodes(extracted)
    leaf_nodes = text_nodes_to_leaf_nodes(text_nodes)
    p_parent = ParentNode("p", leaf_nodes)
    blockquote_parent = ParentNode("blockquote", [p_parent])
    # blockquote_parent = ParentNode("blockquote", leaf_nodes)
    return blockquote_parent

#####################
# Quote function used for passing the test
#####################
# def extract_quote(block):
#     lines = block.split("\n")
#     new_lines = []
#     for line in lines:
#         if not line.startswith(">"):
#             raise ValueError("invalid quote block")
#         new_lines.append(line.lstrip(">").strip())
#     print("new_lines", new_lines)
#     content = " ".join(new_lines)
#     print("content", content)
#     return content

# def quote_to_html(quote_block):
#     extracted = extract_quote(quote_block)
#     # print("extracted", f"${extracted}$")
#     text_nodes = text_to_textnodes(extracted)
#     leaf_nodes = text_nodes_to_leaf_nodes(text_nodes)
#     blockquote_parent = ParentNode("blockquote", leaf_nodes)
#     return blockquote_parent

#############################
# PARAGRAPH FUNCTION
#############################
def paragraph_to_html(p_block):
    text_nodes = text_to_textnodes(p_block)
    leaf_nodes = text_nodes_to_leaf_nodes(text_nodes)
    p_parent = ParentNode("p", leaf_nodes)
    return p_parent

#############################
# HEAD TAG FUNCTION
#############################
def create_head_node():
    return ParentNode("head", [
        HTMLNode("meta", None, None, {
            "charset": "utf-8"
        }),
        HTMLNode("meta", None, None, {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0"
        }),
        LeafNode("title", "title of website"),
        HTMLNode("link", None, None, {
            "href": "styles.css",
            "rel": "stylesheet",
            "type": "text/css"
        }),
        HTMLNode("script", None, None, {
            "src": "script.js",
            "type": "module"
        })
        ]
    )

#############################
# EXTRACT TITLE FUNCTION
#############################
def extract_title(markdown):
    if markdown.startswith("# ", 0, 2):
        first_line = markdown.split("\n", 1)[0]

        header_type, header = first_line.split(" ", 1)

        if header_type == "#":
            return header.strip()
    else:
        raise Exception("Heading 1 must be present on the first line")

#############################
# MAIN FUNCTION
#############################
def markdown_to_html_node(markdown, include_head=False):
    if type(include_head) != bool:
        raise TypeError(f"'include_head' argument is of type '{type(include_head).__name__}', but must be a boolean.")
    body_child_list = []

    block_list = markdown_to_blocks(markdown)
    # print("block_lists", block_list)

    for block in block_list:
        block_type = block_to_block_type(block)
        # print("block_type", block_type)

        match block_type:
            case "heading":
                heading_html = heading_to_html(block)
                body_child_list.append(heading_html)

            case "unordered_list":
                li_nodes = list_to_html(block)
                ul_parent = ParentNode("ul", li_nodes)
                body_child_list.append(ul_parent)
            
            case "ordered_list":
                li_nodes = list_to_html(block)
                ul_parent = ParentNode("ol", li_nodes)
                body_child_list.append(ul_parent)

            case "code":
                code_node = code_to_html(block)
                body_child_list.append(code_node)

            case "quote":
                quote_node = quote_to_html(block)
                body_child_list.append(quote_node)

            case "paragraph":
                p_node = paragraph_to_html(block)
                body_child_list.append(p_node)

    # body_node = ParentNode("body", body_child_list)
    article_node = ParentNode("article", body_child_list)

    return ParentNode("body", [article_node])

    # if include_head:
    #     head_node = create_head_node()

    #     return ParentNode('html', [head_node, body_node])
    # else:
    #     return ParentNode('html', [body_node])

#############
# Code to pass the specific tests for the course
#############
# def markdown_to_html_node(markdown, include_head=False):
#     if type(include_head) != bool:
#         raise TypeError(f"'include_head' argument is of type '{type(include_head).__name__}', but must be a boolean.")
#     body_child_list = []

#     block_list = markdown_to_blocks(markdown)
#     # print("block_lists", block_list)

#     for block in block_list:
#         block_type = block_to_block_type(block)
#         # print("block_type", block_type)

#         match block_type:
#             case "heading":
#                 heading_html = heading_to_html(block)
#                 body_child_list.append(heading_html)

#             case "unordered_list":
#                 li_nodes = list_to_html(block)
#                 ul_parent = ParentNode("ul", li_nodes)
#                 body_child_list.append(ul_parent)
            
#             case "ordered_list":
#                 li_nodes = list_to_html(block)
#                 ul_parent = ParentNode("ol", li_nodes)
#                 body_child_list.append(ul_parent)

#             case "code":
#                 code_node = code_to_html(block)
#                 body_child_list.append(code_node)

#             case "quote":
#                 quote_node = quote_to_html(block)
#                 body_child_list.append(quote_node)

#             case "paragraph":
#                 p_node = paragraph_to_html(block)
#                 body_child_list.append(p_node)

#     return ParentNode("html", body_child_list)
