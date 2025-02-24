import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        node1 = HTMLNode("div", "Hi there", None, {"class": "greeting", "href": "https://boot.dev"})

        node2 = HTMLNode("meta", None, None, {
            "charset": "utf-8"
        })
        self.assertEqual(node1.tag, "div")

        self.assertEqual(node1.value, "Hi there")

        self.assertEqual(node1.children, None)

        self.assertEqual(node1.props, {"class": "greeting", "href": "https://boot.dev"})

        self.assertEqual(node2.to_html(), '<meta charset="utf-8"  />')
    
    def test_value_type_exceptions(self):
        with self.assertRaises(ValueError) as invalid_tag_value:
            HTMLNode([])
        self.assertEqual(str(invalid_tag_value.exception), "Tag argument must be a string value")
        
        with self.assertRaises(ValueError) as invalid_value_value:
            HTMLNode(None, [])
        self.assertEqual(str(invalid_value_value.exception), "Value argument must be a string value")

        with self.assertRaises(ValueError) as invalid_list_value:
            HTMLNode(None, None, "")
        self.assertEqual(str(invalid_list_value.exception), "Children argument must be a list")

        with self.assertRaises(ValueError) as invalid_props_type:
            HTMLNode(None, None, None, "invalid dict value")
        self.assertEqual(str(invalid_props_type.exception), "Props argument must be a dictionary")

    def test_props_to_string(self):
        # Test empty props
        node1 = HTMLNode()
        self.assertEqual(node1.props_to_html(), "")
        
        # Test correct string format
        node2 = HTMLNode(props={"href": "https://www.google.com",
    "target": "_blank",})
        correct_attribute_string =' href="https://www.google.com" target="_blank" '
        self.assertEqual(node2.props_to_html(), correct_attribute_string)

    def test_exception(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode("bad_tag").to_html()

    def test_repr(self):
        node = HTMLNode("h1", "I am a Title", props={"class":"header", "id": "main-header"})

        correct_repr = "HTMLNode(h1, I am a Title, children: None, {'class': 'header', 'id': 'main-header'})"

        self.assertEqual(node.__repr__(), correct_repr)

    ############################
    # LeafNode Tests
    def test_leaf_format(self):
        text_leaf = LeafNode(None, "Hello World")
        self.assertEqual(text_leaf.to_html(), "Hello World")
        
        p_leaf = LeafNode("p", "Hello World")
        self.assertEqual(p_leaf.to_html(), '<p>Hello World</p>') 

        a_leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})        
        self.assertEqual(a_leaf.to_html(), '<a href="https://www.google.com" >Click me!</a>')

        img_leaf = LeafNode('image', None, {"src": "/images"})
        self.assertEqual(img_leaf.to_html(), '<img  src="/images" />')
        with self.assertRaises(ValueError):
            LeafNode('image', None, {})
        with self.assertRaises(ValueError):
            LeafNode('image', None, {"src": ""})

    def test_leaf_repr(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf.__repr__(), "LeafNode(a, Click me!, {'href': 'https://www.google.com'})")

    ############################
    # ParentNode Tests
    def test_parent_params(self):
        #Test No Tag Value:
        with self.assertRaises(ValueError) as no_tag_err_message:
            ParentNode("")
        self.assertEqual(str(no_tag_err_message.exception), "Tag is required")

        #Test No Child Value:
        with self.assertRaises(ValueError) as no_child_err_message:
            ParentNode("p")
        self.assertEqual(str(no_child_err_message.exception), "Children are required")

    def test_parent_html_string(self):
        #HTML Parent
        html_parent = ParentNode("html", [LeafNode(None, "some text")])

        self.assertEqual(html_parent.to_html(), '<!DOCTYPE html><html>some text</html>')
        
        #Basic Parent:
        children_list = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
        ]

        basic_parent = ParentNode(
            "div",
            children_list,
        )
        correct_html_string = '<div><b>Bold text</b>Normal text</div>'
        self.assertEqual(basic_parent.to_html(), correct_html_string)

        #Parent - Child - Grandchild:
        child = LeafNode("b", "Bold text")
        grandchild = LeafNode(None, "Normal text")
        nested_parents = ParentNode(
            "div",
            [
                child,
                ParentNode(
                    "div",
                    [
                        grandchild,
                    ],
                )
            ],
        )

        correct_html_string = '<div><b>Bold text</b><div>Normal text</div></div>'
        self.assertEqual(nested_parents.to_html(), correct_html_string)

    def test_parent_repr(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
            {"class": "parent-div"}
        )
        correct_printing = "ParentNode(div, [LeafNode(b, Bold text, None), LeafNode(None, Normal text, None)], {'class': 'parent-div'})"
        self.assertEqual(node.__repr__(), correct_printing)




