from enum import Enum
from src.htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other_node):
        is_equal = self.text == other_node.text and self.text_type == other_node.text_type and self.url == other_node.url
        return is_equal
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

        
def text_node_to_html_node(text_node):    
    if not isinstance(text_node, TextNode):
        raise ValueError("Argument must be an instance of TextNode")
    
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("Url is required for links")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if not text_node.text:
                raise ValueError("Text is required to use as alt text for images") 
            if not text_node.url:
                raise ValueError("Url is required for images") 
            return LeafNode("img", None, {"alt": text_node.text, "src": text_node.url, "title": text_node.text})
        case _ :
            raise ValueError(f"Invalid text type: {text_node.text_type}")
        


