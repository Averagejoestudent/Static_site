from enum import Enum
from textnode import text_node_to_html_node
from newcode import text_to_textnodes
from htmlnode import ParentNode
import re

class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children_html_nodes = []
    for text_node in text_nodes:
        children_html_nodes.append(text_node_to_html_node(text_node))
    return children_html_nodes




def Heading_Block(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    heading = block[count:].strip()
    children = text_to_children(heading)
    return ParentNode(f"h{count}", children)

def Paragraph_Block(block):
    children = text_to_children(block)
    return ParentNode("p",children)

def Code_Block(block):
    pass

def Olist_Block(block):
    pass

def Ulist_Block(block):
    pass

def Quote_Block(block):
    pass

def markdown_to_html_node(markdown):
     list_of_blocks = markdown_to_blocks(markdown)
     html_node_list = []
     for block in list_of_blocks:
        type_of_block = block_to_block_type(block)
        if type_of_block == BlockType.HEADING:
            html_node = Heading_Block(block)
        elif type_of_block == BlockType.CODE:
            html_node = Code_Block(block)
        elif type_of_block == BlockType.PARAGRAPH:
            html_node = Paragraph_Block(block)
        elif type_of_block == BlockType.QUOTE:
            html_node = Quote_Block(block)
        elif type_of_block == BlockType.OLIST:
            html_node = Olist_Block(block)
        elif type_of_block == BlockType.ULIST:
            html_node = Ulist_Block(block)
        if html_node:
            html_node_list.append(html_node)
