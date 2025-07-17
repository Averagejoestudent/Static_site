from enum import Enum
from textnode import text_node_to_html_node
from newcode import text_to_textnodes
from htmlnode import ParentNode , LeafNode
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
    block = block.replace("\n", " ")
    children = text_to_children(block)
    return ParentNode("p",children)

def Code_Block(block):
    code_content = block[3:-3]
    if code_content.startswith('\n'):
        code_content = code_content[1:]
    raw_code_leaf = LeafNode(None, code_content)
    code_html = ParentNode("code", [raw_code_leaf])
    return ParentNode("pre", [code_html])

def Olist_Block(block):
    lines = block.split('\n')
    list_items = []
    for i, line in enumerate(lines):
        dot_index = line.find('.')
        space_index = line.find(' ', dot_index + 1)
        item_text = line[space_index + 1:]
        children = text_to_children(item_text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)


def Ulist_Block(block):
    lines = block.split('\n')
    list_items = []
    for line in lines:
        item_text = line[2:]
        children = text_to_children(item_text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)


def Quote_Block(block):
    lines = block.split('\n')
    processed_lines = [line[1:].strip() for line in lines] # Remove '>' and strip
    processed_text = "\n".join(processed_lines)
    children = text_to_children(processed_text)
    return ParentNode("blockquote", children)

def markdown_to_html_node(markdown):
    list_of_blocks = markdown_to_blocks(markdown)
    if not list_of_blocks:
       return LeafNode("div","")

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
        else:
            raise ValueError(f"Unknown block type")
        if html_node:
            html_node_list.append(html_node)
    parent_div = ParentNode("div", html_node_list)
    return parent_div
