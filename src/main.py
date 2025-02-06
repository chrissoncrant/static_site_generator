from textnode import TextNode
from htmlnode import HTMLNode, LeafNode

def main():
    print("Main running...")
    p_leaf = LeafNode("p", "Hello World", {"class": "hello"})
    # print(p_leaf.to_html())

    a_leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    # print(a_leaf.to_html())

    img_leaf3 = LeafNode('image', None, {"src": "/images"})

    # print(img_leaf3.to_html())

if __name__ == "__main__":
    main()