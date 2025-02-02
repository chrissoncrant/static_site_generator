from textnode import TextNode

def main():
    print("Main running...")
    new_node = TextNode("Hello!", "bold")
    new_node2 = TextNode("Hello!", "bold")

    print(new_node.__repr__())

    # print(new_node)

if __name__ == "__main__":
    main()