from htmlnode import *
from textnode import *
from inline_markdown import *
from markdown_blocks import *


def markdown_to_html_node(markdown):
    
    blocks = markdown_to_blocks(markdown)
    htmlnodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            children = text_to_children(block, block_type)
            heading_level_tag = heading_level(block)
            htmlnode = ParentNode(heading_level_tag, children)
            #print(htmlnode)
            htmlnodes.append(htmlnode)
        elif block_type == BlockType.CODE:
            #print(block)
            code = block.replace("```\n", "")
            code = code.replace("```", "")
            #print(code)
            textnode = TextNode(code, TextType.CODE)
            child = text_node_to_html_node(textnode)
            htmlnode = ParentNode("pre", child)
            htmlnodes.append(htmlnode)
        elif block_type == BlockType.QUOTE:
            children = text_to_children(block, block_type)
            htmlnode = ParentNode("blockquote", children)
            #print(htmlnode)
            htmlnodes.append(htmlnode)
        elif block_type == BlockType.ULIST:
            children = text_to_list_items(block, block_type)
            htmlnode = ParentNode("ul", children)
            htmlnodes.append(htmlnode)
        elif block_type == BlockType.OLIST:
            children = text_to_list_items(block, block_type)
            htmlnode = ParentNode("ol", children)
            htmlnodes.append(htmlnode)
        else:
            children = text_to_children(block)
            htmlnode = ParentNode("p", children)
            #print(htmlnode)
            htmlnodes.append(htmlnode)

    parent = ParentNode("div", htmlnodes)
    return parent


def text_to_children(text, block_type=None):
    children = []
    nodes = text_to_textnodes(text)
    #print(nodes)
    for node in nodes:
        if block_type == BlockType.HEADING:
            node.text = node.text.lstrip("#")
            node.text = node.text.lstrip()
        if block_type == BlockType.QUOTE:
            node.text = node.text.replace(">", "")
        if block_type == BlockType.PARAGRAPH or block_type is None:
            node.text = node.text.replace("\n", " ")
        children.append(text_node_to_html_node(node))

    return children

def text_to_list_items(text, block_type=None):
    parents = []
    #print(text)
    lines = text.splitlines()
    if block_type == BlockType.ULIST:
        for line in lines:
            children = []
            line = line.replace("- ", "")
            nodes = text_to_textnodes(line)
            for node in nodes:
                children.append(text_node_to_html_node(node))
            parents.append(ParentNode("li", children))
    elif block_type == BlockType.OLIST:
        i = 1
        for line in lines:
            children = []
            line = line.replace(f"{i}. ", "")
            nodes = text_to_textnodes(line)
            for node in nodes:
                children.append(text_node_to_html_node(node))
            parents.append(ParentNode("li", children))
            i += 1
            
    return parents

def heading_level(text):
    if text.startswith("######"):
        return "h6"
    elif text.startswith("#####"):
        return "h5"
    elif text.startswith("####"):
        return "h4"
    elif text.startswith("###"):
        return "h3"
    elif text.startswith("##"):
        return "h2"
    elif text.startswith("#"):
        return "h1"
    else:
        return None