from htmlnode import *
from textnode import *
from inline_markdown import *
from markdown_blocks import *


def markdown_to_html_node(markdown):
    
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            pass
        elif block_type == BlockType.CODE:
            pass
        elif block_type == BlockType.QUOTE:
            pass
        elif block_type == BlockType.ULIST:
            pass
        elif block_type == BlockType.OLIST:
            pass
        elif block_type == BlockType.CODE:
            pass