from src.textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    if type(old_nodes) != list:
        raise ValueError("old_nodes argument must be a list")
    
    if len(old_nodes) == 0:
        raise ValueError("old_nodes list is empty")
   
    allowed_delimiters = ["*", "**", "`"]
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
        "*": TextType.ITALIC,
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
                delimited_node = TextNode(split_text[i], text_type)
                new_nodes.append(delimited_node)
                continue
            text_node = TextNode(split_text[i], TextType.TEXT)
            new_nodes.append(text_node)
    return new_nodes