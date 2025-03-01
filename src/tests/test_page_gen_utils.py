import unittest

from src.generate_pages import create_rel_path_string, replace_image_links

class TestPageGenerationUtilities(unittest.TestCase):
    def test_rel_path_string(self):
        result = create_rel_path_string("images", "img.png")
        correct_result = "./img.png"
        self.assertEqual(result, correct_result)

        result = create_rel_path_string("public/blog/glorfindel/index.html", "index.css")
        correct_result = "../../index.css"
        self.assertEqual(result, correct_result)

    def test_replace_image_links(self):
        des_path = "public/blog/glorfindel/index.html"
        img_1 = '<img  alt="test_1" src="[? ./images/test_1.png ?]" title="test_1" />'
        img_2 = '<img  alt="test_2" src="[? ./images/test_2.png ?]" title="test_2" />'        
        
        # Single Image
        result = replace_image_links(img_1, des_path)
        correct_result = '<img  alt="test_1" src="../../images/test_1.png" title="test_1" />'
        self.assertEqual(result, correct_result)
        
        # Multiple Images of Same Image
        result = replace_image_links((img_1 + img_1), des_path)
        correct_result = '<img  alt="test_1" src="../../images/test_1.png" title="test_1" /><img  alt="test_1" src="../../images/test_1.png" title="test_1" />'
        self.assertEqual(result, correct_result)

        # Multiple Images
        result = replace_image_links((img_1 + img_2), des_path)
        correct_result = '<img  alt="test_1" src="../../images/test_1.png" title="test_1" /><img  alt="test_2" src="../../images/test_2.png" title="test_2" />'
        self.assertEqual(result, correct_result)