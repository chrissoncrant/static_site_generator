import unittest
from src.block_markdown import markdown_to_blocks, block_to_block_type

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

class TestBlockToBlockType(unittest.TestCase):

    def test_code_blocks(self):
        block1 = '```python\ndef add(x, y):    # This is a function\n    return x + y\n```'
        result1 = block_to_block_type(block1)
        self.assertEqual(result1, "code")

        block2 = '```python\ndef add(x, y):    # This is a function\n    return x + y\n'
        result2 = block_to_block_type(block2)
        self.assertEqual(result2, "paragraph")

        block3 = "Plain paragraph"
        result3 = block_to_block_type(block3)
        self.assertEqual(result3, "paragraph")

    def test_quote_blocks(self):
        quote1 = '> This is a block quote. It has some **bold** and *italic* words inside of it.\n>Here is another line of the quote'
        result1 = block_to_block_type(quote1)
        self.assertEqual(result1, "quote")

        quote2 = '>This is a block quote. It has some **bold** and *italic* words inside of it.\nHere is another line of the quote'
        result2 = block_to_block_type(quote2)
        self.assertEqual(result2, "paragraph")

        quote3 = '> This is a block quote. It has some **bold** and *italic* words inside of it.\n\n> Here is another line of the quote'
        result3 = block_to_block_type(quote3)
        self.assertEqual(result3, "paragraph")

    def test_heading_blocks(self):
        heading_blocks = ['# Heading 1', '## Heading 2', '### Heading 3', '#### Heading 4', '##### Heading 5', '###### Heading 6', '####### Attempted Heading', '#####AttemptedHeading ', '#', '# Heading # Still A Heading']
        
        results = []
        for heading in heading_blocks:
            block_type = block_to_block_type(heading)
            results.append(block_type)

        correct_results = ['heading', 'heading', 'heading', 'heading', 'heading', 'heading', 'paragraph', 'paragraph', 'paragraph', 'heading']
        self.assertListEqual(results, correct_results)

    def test_ordered_list_blocks(self):
        ordered_list_block1 = '1. This is the first list item in a list block\n2. This is a list item\n3. This is a list item\n4. This is a list item\n5. This is a list item\n6. This is a list item\n7. This is a list item\n8. This is a list item\n9. This is a list item\n10. This is a list item'

        ordered_list_block2 = '1. This is the first list item in a list block\n2. This is a list item\n3. This is a list item\n4. This is a list item\n5. This is a list item\n6. This is a list item\n7. This is a list item\n8. This is a list item\n9. This is a list item\n10. This is a list item\n1. another line'

        ordered_list_block3 = '1. This is the first list item in a list block\n3. This is a list item'

        ordered_list_block4 = '1. This is the first list item in a list block\n2.This is a list item'

        ordered_list_block5 = '1. This is the first list item in a list block\n\n2. This is a list item'

        ordered_list_tests = [ordered_list_block1, ordered_list_block2, ordered_list_block3, ordered_list_block4, ordered_list_block5]

        correct_results = ['ordered_list', 'paragraph', 'paragraph', 'paragraph', 'paragraph']

        results = []
        
        for test_list in ordered_list_tests:
            block_type = block_to_block_type(test_list)
            results.append(block_type)

        self.assertListEqual(results, correct_results)

    def test_unordered_list_blocks(self):
        unordered_list_block1 = '- This is the first list item in a list block\n* This is a list item\n* This is the last list item'

        unordered_list_block2 = '- This is the first list item in a list block\n\n* This is a list item\n* This is the last list item'

        unordered_list_block3 = '- This is the first list item in a list block\n*This is a list item\n* This is the last list item'

        unordered_list_block4 = '- This is the first list\nNew line'

        plain_paragraph = "Plain paragraph"

        unordered_list_tests = [unordered_list_block1, unordered_list_block2, unordered_list_block3, unordered_list_block4, plain_paragraph]

        correct_results = ['unordered_list', 'paragraph', 'paragraph', 'paragraph', 'paragraph']

        results = []

        for test_list in unordered_list_tests:
            block_type = block_to_block_type(test_list)
            results.append(block_type)
        self.assertListEqual(results, correct_results)
