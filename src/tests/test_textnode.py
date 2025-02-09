import unittest

from src.textnode import TextNode, TextType, text_node_to_html_node

from src.inline_markdown import split_nodes_delimiter
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        # Create two instances
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)

        # Run the __eq__ method on node using node2 as other
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected_repr = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), expected_repr)

    def test_invalid_text_type(self):
        with self.assertRaises(ValueError):
            TextNode("This is a text node", 'ital')

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("TextNode text", "text")
        html_text_node = text_node_to_html_node(text_node)

        self.assertEqual(None, html_text_node.tag)
        self.assertEqual(text_node.text, html_text_node.value)

    def test_bold(self):
        bold_node = TextNode("Bold text", "bold")
        html_bold_node = text_node_to_html_node(bold_node)

        self.assertEqual("b", html_bold_node.tag)
        self.assertEqual(bold_node.
        text, html_bold_node.value)

    def test_italic(self):
        italic_node = TextNode("Italic text", "italic")
        html_italic_node = text_node_to_html_node(italic_node)

        self.assertEqual("i", html_italic_node.tag)
        self.assertEqual(italic_node.
        text, html_italic_node.value)

    def test_code(self):
        code_node = TextNode("code text", "code")
        html_code_node = text_node_to_html_node(code_node)

        self.assertEqual("code", html_code_node.tag)
        self.assertEqual(code_node.
        text, html_code_node.value)

    def test_link(self):
        link_node = TextNode("link text", "link", "https://url.com")
        html_link_node = text_node_to_html_node(link_node)

        self.assertEqual("a", html_link_node.tag)
        self.assertEqual(link_node.
        text, html_link_node.value)
        self.assertEqual(html_link_node.props["href"], link_node.url)

    def test_image(self):
        image_node = TextNode("Alt text", "image", "./path_to_image")
        html_image_node = text_node_to_html_node(image_node)

        self.assertEqual("img", html_image_node.tag)
        self.assertEqual(None, html_image_node.value)
        self.assertEqual(html_image_node.props["alt"], image_node.text)
        self.assertEqual(html_image_node.props["src"], image_node.url)
    
    def test_valid_text_nodes(self):
        with self.assertRaises(ValueError) as invalid_input:
            text_node_to_html_node("invalid input")
        self.assertEqual(str(invalid_input.exception), "Argument must be an instance of TextNode")

        invalid_text_type = TextNode("text", "text")
        invalid_text_type.text_type = "invalid type"
        with self.assertRaises(ValueError) as invalid_type:
            text_node_to_html_node(invalid_text_type)
        self.assertEqual(str(invalid_type.exception), "Invalid text type: invalid type")

        invalid_link_url = TextNode("link text", "link")
        with self.assertRaises(ValueError) as invalid_url:
            text_node_to_html_node(invalid_link_url)
        self.assertEqual(str(invalid_url.exception), "Url is required for links")

        invalid_image_missing_text = TextNode("", "image", "url")
        with self.assertRaises(ValueError) as missing_text:
            text_node_to_html_node(invalid_image_missing_text)
        self.assertEqual(str(missing_text.exception), "Text is required to use as alt text for images")

        invalid_image_src = TextNode("alt text", "image", "")
        with self.assertRaises(ValueError) as missing_url:
            text_node_to_html_node(invalid_image_src)
        self.assertEqual(str(missing_url.exception), "Url is required for images")

if __name__ == "__main__":
    unittest.main()