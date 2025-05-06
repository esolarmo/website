import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

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
        block = "```\nThis is code\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> This is\n> a multi\n> line quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered(self):
        block = "- This is\n- an unordered\n- list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ULIST)
    
    def test_block_to_block_type_ordered(self):
        block = "1. This is\n2. an unordered\n3. list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.OLIST)
    
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