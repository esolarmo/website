from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    block_list = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if not block.isspace() and block != "":
            block_list.append(block)
    #print(block_list)
    return block_list

def block_to_block_type(block):
    if re.match(r"(^#{1,6} )", block) != None:
        return BlockType.HEADING
    if re.match(r"(^`{3}).*(`{3}$)", block) != None:
        return BlockType.CODE
    quote = False
    lines = block.splitlines()
    for line in lines:
        if line.startswith(">"):
            quote = True
        else:
            quote = False
            break
    if quote == True:
        return BlockType.QUOTE
    
    unordered_list = False
    lines = block.splitlines()
    for line in lines:
        if line.startswith("- "):
            unordered_list = True
        else:
            unordered_list = False
            break
    if unordered_list == True:
        return BlockType.ULIST
    
    ordered_list = False
    lines = block.splitlines()
    for i in range(len(lines)):
        if lines[i].startswith(f"{i+1}. "):
            ordered_list = True
        else:
            ordered_list = False
            break
    if ordered_list == True:
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH
    
   