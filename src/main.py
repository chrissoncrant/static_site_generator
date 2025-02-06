from textnode import TextType, TextNode, text_node_to_html_node
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


if __name__ == "__main__":
    main()