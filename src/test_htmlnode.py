import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        props = {
                "href": "https://www.google.com",
                "target": "_blank",
                }
        node = HTMLNode(None, None, None, props)

        expected_value = ' href="https://www.google.com" target="_blank"'

        return_value = node.props_to_html()
        
        self.assertEqual(expected_value, return_value)

    def test_eq2(self):
        node = HTMLNode(None, None, None, None)

        expected_value = ""

        return_value = node.props_to_html()
        
        self.assertEqual(expected_value, return_value)




if __name__ == "__main__":
    unittest.main()