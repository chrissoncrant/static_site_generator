class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        # These properties all default to None; a Node with no tag will render as raw text; no value renders as empty tag or is assumed to be a parent, such as a div; no children will assume that the tag has a value; no attributes is also explanatory
        
        # String; HTML tag
        self.tag = tag

        # String; content of the tag
        self.value = value

        # List of HTMLNode instances that are children to this instance
        self.children = children

        # Dictionary; key-value pairs representing the attributes for the tag of this instance
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):        
        if self.props is None:
            return ""
        
        prop_string = ""
        
        for key, value in self.props.items():
            prop_string += f' {key}="{value}"'
        
        return f"{prop_string} "
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value)
        self.props = props

        if self.tag == "img" or self.tag == "image":
            self.validate_image_tag()

    def validate_image_tag(self):
        if self.tag == "image":
            self.tag = "img"

        if self.tag == "img" and ("src" not in self.props or not self.props["src"]):
            raise ValueError("img tags must have a source (src) prop value")

    def to_html(self):

        if self.value is None and self.tag is not "img":
            raise ValueError("LeafNode must have a value")
        
        if self.tag is None:
            return self.value
        
        attributes = self.props_to_html()
        
        if self.tag == "img":
            return f"<img {attributes} />"
        
        return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
