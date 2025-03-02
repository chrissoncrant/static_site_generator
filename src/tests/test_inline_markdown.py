import unittest

from src.inline_markdown import split_nodes_delimiter, find_md_images, find_md_links, split_nodes_images, split_nodes_links, text_to_textnodes

from src.textnode import TextType, TextNode

class TestSplitDelimiter(unittest.TestCase):
    def test_input_value_errors(self):
        test_node = TextNode("I am text", "text")           
        
        with self.assertRaises(ValueError) as invalid_input:
            split_nodes_delimiter([test_node], "/", TextType.TEXT)
        self.assertEqual(str(invalid_input.exception), "invalid delimiter value: /. Only ['_', '**', '`'] delimiters can be used")            
        
        with self.assertRaises(ValueError) as invalid_input:
            split_nodes_delimiter([test_node], "_", TextType.BOLD)
        self.assertEqual(str(invalid_input.exception), "delimiter _ does not match the text_type TextType.BOLD provided")       

    def test_splitting(self):
        test_plain = TextNode("plain text, no delimiters", TextType.TEXT)
        test_non_text = TextNode("not of TextType.TEXT", TextType.BOLD)
        test_lone_word = TextNode("**bold**", TextType.TEXT)
        test_bold = TextNode("Testing node with **bold section** in the middle.", TextType.TEXT)
        test_multiple_bold = TextNode("Testing node with **bold section** in the middle. And **another bold** section.", TextType.TEXT)
        test_italic = TextNode("Testing node with _italic section_ in the middle.", TextType.TEXT)
        test_code = TextNode("Testing node with `code section` in the middle.", TextType.TEXT)

        plain_result = split_nodes_delimiter([test_plain], "**", TextType.BOLD)
        self.assertListEqual([TextNode("plain text, no delimiters", "text", None)], plain_result)

        non_text_result = split_nodes_delimiter([test_non_text], "**", TextType.BOLD)
        self.assertListEqual([TextNode("not of TextType.TEXT", "bold", None)], non_text_result)

        lone_word_result = split_nodes_delimiter([test_lone_word], "**", TextType.BOLD)
        self.assertListEqual(lone_word_result, [TextNode("bold", "bold", None)])

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

        italic_result = split_nodes_delimiter([test_italic], "_", "italic")
        correct_italic_result = [
            TextNode("Testing node with ", "text", None), 
            TextNode("italic section", "italic", None), 
            TextNode(" in the middle.", "text", None)]
        self.assertListEqual(correct_italic_result, italic_result)
        
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

class TestLinkAndImageMarkdownParse(unittest.TestCase):
    def test_input_errors(self):
        with self.assertRaises(ValueError) as invalid_input:
            find_md_links([])
        self.assertEqual(str(invalid_input.exception), "argument must be a string") 
        
        with self.assertRaises(ValueError) as invalid_input:
            find_md_images([])
        self.assertEqual(str(invalid_input.exception), "argument must be a string") 
    
    def test_values(self):
        test_text = "[the official Markdown guide](https://www.markdownguide.org) and a ![Sample Image](images/sample-image.jpg \"testing\")"

        link_list = find_md_links(test_text)

        self.assertListEqual(link_list, [('the official Markdown guide', 'https://www.markdownguide.org')])

        image_list = find_md_images(test_text)

        self.assertListEqual(image_list, [('Sample Image', 'images/sample-image.jpg "testing"')])

class TestImageSplit(unittest.TestCase):
    def test_input_errors(self):
        with self.assertRaises(ValueError) as invalid_input:
            split_nodes_images([""])
        self.assertEqual(str(invalid_input.
        exception), "Item \"\" must be an instance of TextNode")

    def test_values(self):
        one_image_node = TextNode(
            "Here is a ![Sample Image1](images/sample1-image.jpg \"testing\"). And here is the last sentence.",
            TextType.TEXT,
        )
        result = split_nodes_images([one_image_node])
        correct_result = [
            TextNode("Here is a ", "text", None), 
            TextNode("Sample Image1", "image", "[? images/sample1-image.jpg ?]"), 
            TextNode(". And here is the last sentence.", "text", None)
        ]
        self.assertListEqual(result, correct_result)

        image_alone = TextNode(
            "![Sample Image1](images/sample1-image.jpg \"testing\")",
            TextType.TEXT
        )
        result = split_nodes_images([image_alone])
        correct_result = [TextNode("Sample Image1", "image", "[? images/sample1-image.jpg ?]")]
        self.assertListEqual(result, correct_result)


        two_image_node = TextNode(
            "Here is a ![Sample Image1](images/sample1-image.jpg \"testing\"). And here is the last sentence. and another image: ![Sample Image2](images/sample2-image.jpg). Last sentence.",
            TextType.TEXT,
        )
        result = split_nodes_images([two_image_node])        
        correct_result = [
            TextNode("Here is a ", "text", None), 
            TextNode("Sample Image1", "image", "[? images/sample1-image.jpg ?]"), 
            TextNode(". And here is the last sentence. and another image: ", "text", None), 
            TextNode("Sample Image2", "image", "[? images/sample2-image.jpg ?]"), 
            TextNode(". Last sentence.", "text", None)
        ]
        self.assertListEqual(result, correct_result)

        image_and_link_node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and a ![Sample Image](images/sample-image.jpg \"testing\")",
            TextType.TEXT,
        )
        result = split_nodes_images([image_and_link_node])
        correct_result = [
            TextNode("This is text with a link [to boot dev](https://www.boot.dev) and a ", "text", None), 
            TextNode("Sample Image", "image", "[? images/sample-image.jpg ?]")
        ]
        self.assertListEqual(result, correct_result)

        plain_node = TextNode(
            "This is just a sentence.",
            TextType.TEXT,
        )
        result = split_nodes_images([plain_node, one_image_node])
        correct_result = [
            TextNode("This is just a sentence.", "text", None),
            TextNode("Here is a ", "text", None), 
            TextNode("Sample Image1", "image", "[? images/sample1-image.jpg ?]"), 
            TextNode(". And here is the last sentence.", "text", None)
        ]
        self.assertListEqual(result, correct_result)

        code_node = TextNode("I am code", TextType.CODE, None)
        result = split_nodes_images([code_node])
        self.assertListEqual(result, [TextNode("I am code", TextType.CODE, None)])

class TestLinkSplit(unittest.TestCase):
    def test_input_errors(self):
        with self.assertRaises(ValueError) as invalid_input:
         split_nodes_links("")
        self.assertEqual(str(invalid_input.
        exception), "argument must be a list") 
        
        with self.assertRaises(ValueError) as invalid_input:
         split_nodes_links([])
        self.assertEqual(str(invalid_input.
        exception), "argument is an empty list") 
        
        with self.assertRaises(ValueError) as invalid_input:
         split_nodes_links([""])
        self.assertEqual(str(invalid_input.
        exception), "Item \"\" must be an instance of TextNode")

    def test_values(self):
        one_link_node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) in the middle.", 
            TextType.TEXT
        )
        result = split_nodes_links([one_link_node])
        correct_result = [
            TextNode("This is text with a link ", "text", None), 
            TextNode("to boot dev", "link", "https://www.boot.dev"), 
            TextNode(" in the middle.", "text", None)
        ]
        self.assertListEqual(result, correct_result)

        link_alone = TextNode(
            "[to boot dev](https://www.boot.dev)", 
            TextType.TEXT
        )
        result = split_nodes_links([link_alone])
        correct_result = [
            TextNode("to boot dev", "link", "https://www.boot.dev")
        ]
        self.assertListEqual(result, correct_result)

        two_link_nodes = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).", 
            TextType.TEXT
        )
        result = split_nodes_links([two_link_nodes])
        correct_result = [
            TextNode("This is text with a link ", "text", None), 
            TextNode("to boot dev", "link", "https://www.boot.dev"), 
            TextNode(" and ", "text", None), 
            TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev"), 
            TextNode(".", "text", None)
        ]
        self.assertListEqual(result, correct_result)

        plain_node = TextNode(
            "This is just a sentence.",
            TextType.TEXT,
        )
        result = split_nodes_links([plain_node, one_link_node])
        correct_result = [
            TextNode("This is just a sentence.", "text", None),
            TextNode("This is text with a link ", "text", None), 
            TextNode("to boot dev", "link", "https://www.boot.dev"), 
            TextNode(" in the middle.", "text", None)
        ]
        self.assertListEqual(result, correct_result)

        code_node = TextNode("I am code", TextType.CODE, None)
        result = split_nodes_links([code_node])
        self.assertListEqual(result, [TextNode("I am code", TextType.CODE, None)])

class TestFullInlineSplit(unittest.TestCase):

    def test_values(self):
        test_text = "**This** is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(test_text)
        correct_result = [
            TextNode("This", "bold", None), 
            TextNode(" is ", "text", None),
            TextNode("text", "bold", None), 
            TextNode(" with an ", "text", None), 
            TextNode("italic", "italic", None), 
            TextNode(" word and a ", "text", None), 
            TextNode("code block", "code", None), 
            TextNode(" and an ", "text", None), 
            TextNode("obi wan image", "image", "[? https://i.imgur.com/fJRm4Vk.jpeg ?]"), 
            TextNode(" and a ", "text", None), 
            TextNode("link", "link", "https://boot.dev")
        ]
        self.assertListEqual(result, correct_result)

