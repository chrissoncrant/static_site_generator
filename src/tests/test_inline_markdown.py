import unittest

from src.inline_markdown import split_nodes_delimiter

from src.textnode import TextType, TextNode

class TestInlineSplit(unittest.TestCase):
    def test_input_value_errors(self):
        test_node = TextNode("I am text", "text")
        
        with self.assertRaises(ValueError) as invalid_input:
            split_nodes_delimiter("", "**", TextType.BOLD)
        self.assertEqual(str(invalid_input.exception), "old_nodes argument must be a list")       
        
        with self.assertRaises(ValueError) as invalid_input:
            split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(str(invalid_input.exception), "old_nodes list is empty")       
        
        with self.assertRaises(ValueError) as invalid_input:
            split_nodes_delimiter([test_node], "/", TextType.TEXT)
        self.assertEqual(str(invalid_input.exception), "invalid delimiter value: /. Only ['*', '**', '`'] delimiters can be used")       
        
        with self.assertRaises(ValueError) as invalid_input:
            split_nodes_delimiter(["invalid data type"], "**", TextType.BOLD)
        self.assertEqual(str(invalid_input.exception), "All items in old_node list must be instances of TextNode")       
        
        with self.assertRaises(ValueError) as invalid_input:
            split_nodes_delimiter([test_node], "*", TextType.BOLD)
        self.assertEqual(str(invalid_input.exception), "delimiter * does not match the text_type TextType.BOLD provided")       

    def test_splitting(self):
        test_plain = TextNode("plain text, no delimiters", TextType.TEXT)
        test_non_text = TextNode("not of TextType.TEXT", TextType.BOLD)
        test_bold = TextNode("Testing node with **bold section** in the middle.", TextType.TEXT)
        test_multiple_bold = TextNode("Testing node with **bold section** in the middle. And **another bold** section.", TextType.TEXT)
        test_italic = TextNode("Testing node with *italic section* in the middle.", TextType.TEXT)
        test_code = TextNode("Testing node with `code section` in the middle.", TextType.TEXT)

        test_node_list = [test_plain, test_non_text, test_bold, test_multiple_bold, test_italic, test_code]

        plain_result = split_nodes_delimiter([test_plain], "**", TextType.BOLD)
        self.assertListEqual([TextNode("plain text, no delimiters", "text", None)], plain_result)

        non_text_result = split_nodes_delimiter([test_non_text], "**", TextType.BOLD)
        self.assertListEqual([TextNode("not of TextType.TEXT", "bold", None)], non_text_result)

        bold_result = split_nodes_delimiter([test_bold], "**", "bold")
        correct_bold_result = [
            TextNode("Testing node with ", "text", None), 
            TextNode("bold section", "bold", None), 
            TextNode(" in the middle.", "text", None)]
        self.assertListEqual(correct_bold_result, bold_result)
        
        multi_bold_result = split_nodes_delimiter([test_multiple_bold], "**", "bold")
        correct_multi_bold_result = [
            TextNode("Testing node with ", "text", None), 
            TextNode("bold section", "bold", None), 
            TextNode(" in the middle. And ", "text", None), 
            TextNode("another bold", "bold", None), 
            TextNode(" section.", "text", None)
        ]
        self.assertListEqual(correct_multi_bold_result, multi_bold_result)

        italic_result = split_nodes_delimiter([test_italic], "*", "italic")
        correct_italic_result = [
            TextNode("Testing node with ", "text", None), 
            TextNode("italic section", "italic", None), 
            TextNode(" in the middle.", "text", None)]
        self.assertListEqual(correct_italic_result, italic_result)
        print(italic_result)
        
        code_result = split_nodes_delimiter([test_code], "`", "code")
        correct_code_result = [
            TextNode("Testing node with ", "text", None), 
            TextNode("code section", "code", None), 
            TextNode(" in the middle.", "text", None)]
        self.assertListEqual(correct_code_result, code_result)

    def test_output_values(self):
        test_bold = TextNode("Testing node with **bold section** in the middle.", TextType.TEXT)
        test_result = split_nodes_delimiter([test_bold], "**", "bold")

        self.assertEqual(type(test_result), list)
        self.assertEqual(isinstance(test_result[0], TextNode), True)

