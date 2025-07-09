from enum import Enum
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

def Heading_Block(block):
    pass

def Paragraph_Block(block):
    pass

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
     for block in list_of_blocks:
        type_of_block = block_to_block_type(block)
        if type_of_block == BlockType.HEADING:
            Heading_Block(block)
        elif type_of_block == BlockType.CODE:
            Code_Block(block)
        elif type_of_block == BlockType.PARAGRAPH:
            Paragraph_Block(block)
        elif type_of_block == BlockType.QUOTE:
            Quote_Block(block)
        elif type_of_block == BlockType.OLIST:
            Olist_Block(block)
        elif type_of_block == BlockType.ULIST:
            Ulist_Block(block)
