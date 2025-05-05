import unittest

from textnode import TextNode, TextType, BlockType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertEqual(node, node2)
    
    def test_noteq3(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a foobar node", TextType.BOLD)
        self.assertNotEqual(node, node2)

class TestTextToHTML(unittest.TestCase):

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
        
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        #print(new_nodes)
        self.assertEqual(str(new_nodes), "[TextNode('This is text with a ', text, None), TextNode('code block', code, None), TextNode(' word', text, None)]")
        

    def test_split_bold(self):
        node = TextNode("**This** is text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        #print(new_nodes)
        self.assertEqual(str(new_nodes), "[TextNode('This', bold, None), TextNode(' is text with a code block word', text, None)]")

    def test_split_italic(self):
        node = TextNode("Split _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        #print(new_nodes)
        self.assertEqual(str(new_nodes), "[TextNode('Split ', text, None), TextNode('italic', italic, None)]")

    def test_image_type(self):
        node = TextNode("Code block", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        #print(new_nodes)
        self.assertEqual(str(new_nodes), "[TextNode('Code block', code, None)]")

    def test_multiple_nodes(self):
        nodes = [TextNode("Code block", TextType.CODE),
                 TextNode("Normal Text with `some code` in it", TextType.TEXT),
                 ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        #print(new_nodes)
        self.assertListEqual(
            [   
                TextNode("Code block", TextType.CODE, None), 
                TextNode("Normal Text with ", TextType.TEXT, None),
                TextNode("some code", TextType.CODE, None), 
                TextNode(" in it", TextType.TEXT, None),
                ], new_nodes)

    def test_wrong_syntax(self):
        node = TextNode("`Code block", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)

    def test_wrong_syntax2(self):
        node = TextNode("**Bold** section of **text", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "**", TextType.BOLD)
        

class TestExtractMarkdownImages(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_2images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images_and_link(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and this is a link [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif")], matches)
        
class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_images_and_link(self):
        matches = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and this is a link [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev","https://www.boot.dev"),("to youtube","https://www.youtube.com/@bootdotdev")],matches)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is an image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_and_link(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is an image [to youtube](https://www.youtube.com) is a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is an image [to youtube](https://www.youtube.com) is a link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_multiple_nodes(self):
        nodes = [TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
            ),
            TextNode(
            "![image2](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
            ),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [google](https://www.google.com) and another [boot.dev](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("google", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "boot.dev", TextType.LINK, "https://boot.dev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_link_only(self):
        node = TextNode(
            "[google](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("google", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )
        
    def test_split_links_multiple_nodes(self):
        nodes = [TextNode(
            "This is text with a link [google](https://www.google.com) and another [boot.dev](https://boot.dev)",
            TextType.TEXT,
            ),
            TextNode("[microsoft.com](https://www.microsoft.com)", TextType.TEXT,),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("google", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "boot.dev", TextType.LINK, "https://boot.dev"
                ),
                TextNode("microsoft.com", TextType.LINK,"https://www.microsoft.com"),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.maxDiff = None
        nodes = text_to_textnodes(text)
        #print(nodes)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_nodes2(self):
        text = "**Boldly** go where _no one_ has gone before"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Boldly", TextType.BOLD),
                TextNode(" go where ", TextType.TEXT),
                TextNode("no one", TextType.ITALIC),
                TextNode(" has gone before", TextType.TEXT),
            ],
            nodes,
        )

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_linebreaks(self):
        md = """

        
This is **bolded** paragraph

             


        This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line     


- This is a list
- with items





"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):

    def test_block_to_block_type_heading(self):
        block = "### Heading 3\n"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "``` CODE BLOCK     ```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> This is\n> a multi\n> line quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered(self):
        block = "- This is\n- an unordered\n- list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ordered(self):
        block = "1. This is\n2. an unordered\n3. list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_paragraph(self):
        block = "1. This is a paragraph\n- in a list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_paragraph2(self):
        block = "#################"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_empty_paragraph(self):
        block = ""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    

if __name__ == "__main__":
    unittest.main()