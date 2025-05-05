from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered_list"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other_node):
        if self.text == other_node.text and self.text_type == other_node.text_type and self.url == other_node.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode('{self.text}', {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {
                                    "src": text_node.url,
                                    "alt": text_node.text,
                                    })
    else:
        raise ValueError(f"invalid text type: {text_node.text_type}")
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if not isinstance(old_nodes,list):
        old_nodes = [old_nodes]
    for node in old_nodes:
        #print(node)
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            delimited_string = node.text.split(delimiter)
            if len(delimited_string) % 2 == 0:
                raise Exception("uneven number of delimiters: not supported")
            i = 0
            for i in range(len(delimited_string)):
                if i == 0 or i % 2 == 0:
                    if delimited_string[i] != "":
                        new_nodes.append(TextNode(delimited_string[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(delimited_string[i], text_type))
                i += 1
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    #print(matches)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    #print(matches)
    return matches

def split_nodes_image(old_nodes):
    images = []
    new_nodes = []
    #print(f"{old_nodes}")
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            #print(f"{node}")
            images = extract_markdown_images(node.text)
            original_text = node.text
            for image in images:
                sections = original_text.split(f"![{image [0]}]({image[1]})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0],TextType.IMAGE,image[1]))
                original_text = sections[1]
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.TEXT))
        else:
            new_nodes.append(node)


    #print(new_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    links = []
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            #print(links)
            original_text = node.text
            for link in links:
                sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0],TextType.LINK,link[1]))
                original_text = sections[1]
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.TEXT))
        else:
            new_nodes.append(node)

    #print(new_nodes)
    return new_nodes

def text_to_textnodes(text):
    nodes = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

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
        return BlockType.UNORDERED_LIST
    
    ordered_list = False
    lines = block.splitlines()
    for i in range(len(lines)):
        if lines[i].startswith(f"{i+1}. "):
            ordered_list = True
        else:
            ordered_list = False
            break
    if ordered_list == True:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    
   