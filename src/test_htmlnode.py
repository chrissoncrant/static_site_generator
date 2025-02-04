import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        # Test empty props
        node1 = HTMLNode()
        self.assertEqual(node1.props_to_html(), "")
        
        # Test correct string format
        node2 = HTMLNode(props={"href": "https://www.google.com",
    "target": "_blank",})
        correct_attribute_string =' href="https://www.google.com" target="_blank" '
        self.assertEqual(node2.props_to_html(), correct_attribute_string)

    def test_values(self):
        node = HTMLNode("div", "Hi there", None, {"class": "greeting", "href": "https://boot.dev"})

        self.assertEqual(type(node.tag), str)
        self.assertEqual(node.tag, "div")

        self.assertEqual(type(node.value), str)
        self.assertEqual(node.value, "Hi there")

        self.assertEqual(node.children, None)

        self.assertEqual(type(node.props), dict)
        self.assertEqual(node.props, {"class": "greeting", "href": "https://boot.dev"})


    def test_exception(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()

    def test_repr(self):
        node = HTMLNode("h1", "I am a Title", props={"class":"header", "id": "main-header"})

        correct_repr = "HTMLNode(h1, I am a Title, children: None, {'class': 'header', 'id': 'main-header'})"

        self.assertEqual(node.__repr__(), correct_repr)

class TestLeafNode(unittest.TestCase):
    def test_leaf_format(self):
        p_leaf = LeafNode("p", "Hello World", {"class": "hello"})
        self.assertEqual(p_leaf.to_html(), '<p class="hello" >Hello World</p>') 

        a_leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})        
        self.assertEqual(a_leaf.to_html(), '<a href="https://www.google.com" >Click me!</a>')

        img_leaf = LeafNode('image', None, {"src": "/images"})
        self.assertEqual(img_leaf.to_html(), '<img  src="/images"  />')
        with self.assertRaises(ValueError):
            LeafNode('image', None, {})
        with self.assertRaises(ValueError):
            LeafNode('image', None, {"src": ""})

    def test_repr(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf.__repr__(), "LeafNode(a, Click me!, {'href': 'https://www.google.com'})")