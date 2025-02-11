from src.textnode import TextNode, TextType
import re
def main():
    print("Main running...")
    def find_md_images(text):
        md_image_pattern_with_title = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'

        return re.findall(md_image_pattern_with_title, text)
    def split_nodes_images(old_nodes):
        if type(old_nodes) != list:
            raise ValueError("argument must be a list")
        
        if len(old_nodes) == 0:
            raise ValueError("argument is an empty list")
        
        new_nodes = []

        for node in old_nodes:

            if not isinstance(node, TextNode):
                raise ValueError(f"Item \"{node}\" must be an instance of TextNode")

            node_text = node.text
            image_data = find_md_images(node_text)

            if len(image_data) == 0:
                new_nodes.append(TextNode(node_text, TextType.TEXT))
                continue

            for i in range(len(image_data)):
                alt_text = image_data[i][0]
                url = image_data[i][1]

                split = node_text.split(f"![{alt_text}]({url})", 1)

                print(split)

                if url.find('"') != -1:
                    url = url.split(' "')[0]
                
                if url.find("'") != -1:
                    url = url.split(" '")[0]

                text_node = TextNode(split[0], TextType.TEXT)
                new_nodes.append(text_node)

                image_node = TextNode(alt_text, TextType.IMAGE, url)
                new_nodes.append(image_node)

                if i == len(image_data) - 1:
                    text_node = TextNode(split[1], TextType.TEXT)
                    new_nodes.append(text_node)
                    continue

                node_text = split[1]           

        return  new_nodes

    one_image_node = TextNode(
                "Here is a ![Sample Image1](images/sample1-image.jpg \"testing\"). And here is the last sentence.",
                TextType.TEXT,
    )

    result = split_nodes_images([one_image_node])

if __name__ == "__main__":
    main()