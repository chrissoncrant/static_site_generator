import unittest
from src.block_markdown import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_input_errors(self):
        with self.assertRaises(ValueError) as invalid_input:
            markdown_to_blocks([])
        self.assertEqual(str(invalid_input.exception), "argument must be a string")
        
        blank_doc1 = ""
        blank_doc2 = """



        """

        with self.assertRaises(ValueError) as invalid_input:
            markdown_to_blocks(blank_doc1)
        self.assertEqual(str(invalid_input.exception), "input string has no content")

        with self.assertRaises(ValueError) as invalid_input:
            markdown_to_blocks(blank_doc2)
        self.assertEqual(str(invalid_input.exception), "input string has no content")

    def test_values(self):
        test_input = "\nI am a block of two paragraphs.\nHere is paragraph 2.\n\n"
        result = markdown_to_blocks(test_input)
        correct_result = ['I am a block of two paragraphs.\nHere is paragraph 2.']
        self.assertListEqual(result, correct_result)

        test_list_input = "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        result = markdown_to_blocks(test_list_input)
        correct_result = ['* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        self.assertListEqual(result, correct_result)

        test_full_input = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is the last list item"
        result = markdown_to_blocks(test_full_input)
        correct_result = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is the last list item']
        self.assertListEqual(result, correct_result)