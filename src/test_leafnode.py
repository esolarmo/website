import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, BOLD world!")
        self.assertEqual(node.to_html(), "<b>Hello, BOLD world!</b>")
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, plain world!")
        self.assertEqual(node.to_html(), "Hello, plain world!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)



if __name__ == "__main__":
    unittest.main()