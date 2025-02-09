from textnode import TextType, TextNode, text_node_to_html_node, split_nodes_delimiter
from htmlnode import HTMLNode, LeafNode
from mock_markdown import test_text

test_text_list = test_text.split("\n")

def main():
    print("Main running...")
    p_leaf = LeafNode("p", "Hello World", {"class": "hello"})
    # print(p_leaf.to_html())

    a_leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    # print(a_leaf.to_html())

    img_leaf3 = LeafNode('image', None, {"src": "/images"})
    # print(img_leaf3.to_html())

    # image_node = text_node_to_html_node(TextNode("", "image", "url"))

    test_text_node = TextNode("This is text with a **bolded phrase** in the middle", "text")

    split_nodes_delimiter([test_text_node], "**", "bold")


if __name__ == "__main__":
    main()