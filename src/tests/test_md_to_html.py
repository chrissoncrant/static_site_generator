import unittest
from src.htmlnode import LeafNode, ParentNode
from src.textnode import TextNode
from src.md_to_html import string_list_to_text_nodes, text_nodes_to_leaf_nodes, code_to_html, extract_list_text, list_to_html, heading_to_html, extract_quote, quote_to_html, paragraph_to_html, create_head_node, markdown_to_html_node, extract_title

class TestHelperFunctions(unittest.TestCase):
    def test_exceptions(self):
        with self.assertRaises(TypeError) as invalid_input:
            string_list_to_text_nodes("string input")
        self.assertEqual(str(invalid_input.
        exception), "Argument is of type 'str', but must be a list.")
        
        with self.assertRaises(TypeError) as invalid_input:
            text_nodes_to_leaf_nodes("string input")
        self.assertEqual(str(invalid_input.
        exception), "Argument is of type 'str', but must be a list.")

        with self.assertRaises(ValueError) as invalid_input:
            text_nodes_to_leaf_nodes(["string input"])
        self.assertEqual(str(invalid_input.
        exception), "Argument's items must be instances of TextNodes")

    def test_outputs(self):
        test_list = ["String of *text*"]
        correct_result = [[TextNode("String of ", "text", None), TextNode("text", "italic", None)]]
        result = string_list_to_text_nodes(test_list)
        self.assertListEqual(result, correct_result)

        correct_result = [LeafNode(None, "String of ", None), LeafNode("i", "text", None)]
        result = text_nodes_to_leaf_nodes([TextNode("String of ", "text", None), TextNode("text", "italic", None)])
        self.assertListEqual(result, correct_result)

class TestCodeFunction(unittest.TestCase):
    def test_output(self):
        code_md = """```code block```"""
        result = code_to_html(code_md)

        correct_result = ParentNode("code", [ParentNode("pre", [LeafNode(None, "code block", None)], None)], None)
        self.assertEqual(result, correct_result)

class TestListFunctions(unittest.TestCase):
    unordered_list_md = "* This is the first list item in a list block\n* This is a **list** item\n* This is another list item"

    ordered_list_md = "1. This is the first list item in a list block\n2. This is a **list** item\n3. This is another list item"
    
    def test_list_extraction(self):
        correct_output = ['This is the first list item in a list block', 'This is a **list** item', 'This is another list item']

        unordered_list_result = extract_list_text(self.unordered_list_md)
        self.assertListEqual(unordered_list_result, correct_output)
        
        ordered_list_result = extract_list_text(self.ordered_list_md)
        self.assertListEqual(ordered_list_result, correct_output)
    
    def test_list_to_html(self):
        test_list = """1. This is a list item"""

        correct_result = [ParentNode("li", [LeafNode(None, "This is a list item", None)], None)]
        result = list_to_html(test_list)
        self.assertEqual(result, correct_result)

class TestHeaderFunction(unittest.TestCase):
    def test_heading_to_html(self):
        heading1_md = "# This is a heading"
        heading4_md = "#### This is a heading"

        correct1 = ParentNode("h1", [LeafNode(None, "This is a heading", None)], None)
        correct2 = ParentNode("h4", [LeafNode(None, "This is a heading", None)], None)

        result1 = heading_to_html(heading1_md)
        result2 = heading_to_html(heading4_md)

        self.assertEqual(result1, correct1)
        self.assertEqual(result2, correct2)

class TestQuoteFunctions(unittest.TestCase):
    quote_md = "> quoting some stuff.\n>And this is a new line."

    def test_extract_quote(self):
        correct_result = "quoting some stuff.\nAnd this is a new line."

        result = extract_quote(self.quote_md)
        self.assertEqual(result, correct_result)

    def test_quote_to_html(self):
        correct_result = ParentNode("blockquote", [ParentNode("p", [LeafNode(None, 'quoting some stuff.\nAnd this is a new line.', None)], None)], None)

        result = quote_to_html(self.quote_md)
        self.assertEqual(result, correct_result)

class TestParagraphFunction(unittest.TestCase):
    def test_paragraph_to_html(self):
        p_md = "This is a paragraph of text."
        correct_result = ParentNode("p", [LeafNode(None, "This is a paragraph of text.", None)], None)

        result = paragraph_to_html(p_md)
        self.assertEqual(result, correct_result)

class TestExtractTitleFunction(unittest.TestCase):
    def test_invalid_input(self):
        with self.assertRaises(Exception) as invalid_input:
            extract_title("## Heading 2")
        self.assertEqual(str(invalid_input.exception), "Heading 1 must be present on the first line")

    def test_extract_title(self):
        correct_result = "Heading 1"
        result = extract_title("# Heading 1")
        self.assertEqual(result, correct_result)

class TestMarkdownToHTMLNode(unittest.TestCase):
    
    def test_invalid_include_head_arg(self):
        with self.assertRaises(TypeError) as invalid_input:
            markdown_to_html_node("I'm a paragraph", "yes")
        self.assertEqual(str(invalid_input.
        exception), "'include_head' argument is of type 'str', but must be a boolean.")
    
    def test_markdown_to_html_node(self):
        # No Head Tag
        correct_result = "<body><article><p>I'm a paragraph</p></article></body>"

        result = markdown_to_html_node("I'm a paragraph").to_html()
        self.assertEqual(result, correct_result)

