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

        # Validating Input Values:
        if type(self.tag) != str and self.tag != None:
            raise ValueError("Tag argument must be a string value")
        if type(self.value) != str and self.value != None:
            raise ValueError("Value argument must be a string value")
        if type(self.children) != list and self.children != None:
            raise ValueError("Children argument must be a list")
        if type(self.props) != dict and self.props != None:
            raise ValueError("Props argument must be a dictionary")
        

    def to_html(self):
        valid_tags = ["head", "meta", "title", "link", "script"]

        if self.tag not in valid_tags:
            raise NotImplementedError
        else:
            attributes = self.props_to_html()

            if self.tag == "script":
                return f"<{self.tag}{attributes}></{self.tag}>"
            
            return f"<{self.tag}{attributes} />"
    
    def props_to_html(self):                
        if self.props is None:
            return ""
        
        prop_string = " "
        
        for key, value in self.props.items():
            prop_string += f'{key}="{value}" '
        
        return f"{prop_string}"
    
    def __eq__(self, other_node):
            is_equal = self.tag == other_node.tag and self.value == other_node.value and self.children == other_node.children and self.props == other_node.props
            return is_equal

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # A mistake I made, was not putting in None for the children parameter, and just put 'props'. What occurred was the props initialized with an instance were actually passed in as the value for the children.
        super().__init__(tag, value, None, props)

        if self.tag == "img" or self.tag == "image":
            self.validate_image_tag()

    def validate_image_tag(self):
        if self.tag == "image":
            self.tag = "img"

        if self.tag == "img" and ("src" not in self.props or not self.props["src"]):
            raise ValueError("img tags must have a source (src) prop value")

    def to_html(self):

        #Image tags don't have values as they are self-closing; but all other Leafs require values
        if self.value is None and self.tag != "img":
            raise ValueError("LeafNode must have a value")
        
        # If tag is none, then even if props are erroneously present, they don't need to be rendered because there is no tag within which to render them. 
        if self.tag is None:
            return self.value
        
        attributes = self.props_to_html()
        
        if self.tag == "img":
            return f"<img {attributes}/>"
        
        return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        
        super().__init__(tag, None, children, props)
        if not self.tag:
            raise ValueError("Tag is required")
        
        if not self.children:
            raise ValueError("Children are required")

        if not isinstance(self.children, list): 
            raise ValueError("Children argument must be a list")

    def to_html(self):
        if self.tag == "html":
            el_string = f"<!DOCTYPE html><{self.tag}{self.props_to_html()}>"
        else:
            el_string = f"<{self.tag}{self.props_to_html()}>"
        for i in range(len(self.children)):
                child_el = self.children[i]
                child_el_string = child_el.to_html()
                el_string += child_el_string
                
        return f"{el_string}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
