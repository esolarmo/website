import unittest
from textnode import TextNode, TextType
from main import text_node_to_html_node

class TestMain(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_invalidtype(self):
        node = TextNode("This is an invalid type node", "foobar")
        self.assertRaises(ValueError, text_node_to_html_node, node)
        