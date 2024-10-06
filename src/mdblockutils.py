

from htmlnode import HTMLNode
from nodeutils import *

block_type_paragraph = "paragraph"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
block_type_code = "code"
block_type_quote = "quote"
block_type_heading = "heading"

def markdown_to_blocks(markdown):
    md_blocks = markdown.splitlines()
    stripped_md_blocks = list(map(lambda block: block.strip(), md_blocks))
    filtered_md_blocks = list(filter(lambda block: block != "", stripped_md_blocks))

    return filtered_md_blocks


def block_to_block_type(block: str):
    if block.startswith("#"):
        header_level = 0
        for c in block:
            if c == " ":
                break
            if c == "#":
                header_level += 1
            else:
                return block_type_paragraph
        if header_level > 0 and header_level < 7:
            return block_type_heading + str(header_level)
        return block_type_paragraph
    elif block.startswith(">"):
        return block_type_quote
    elif block.startswith("```") and block.endswith("```"):
        return block_type_code
    elif block.startswith("* ") or block.startswith("- "):
        return block_type_unordered_list
    elif block.startswith("1. ") or block.startswith("1) "):
        return block_type_ordered_list
    else:
        return block_type_paragraph


def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    root = HTMLNode(tag="div", value=None, children=[], props=None)
    for block in md_blocks:
        block_type = block_to_block_type(block)

        if block_type == block_type_unordered_list:
            new_block = HTMLNode(tag="ul", value=None, children=[], props=None)
            root.children.append(new_block)
        elif block_type == block_type_ordered_list:
            new_block = HTMLNode(tag="ol", value=None, children=[], props=None)
            root.children.append(new_block)
        elif block_type == block_type_code:
            new_block = HTMLNode(tag="code", value=block, children=[], props=None)
            root.children.append(new_block)
        elif block_type == block_type_quote:
            new_block = HTMLNode(tag="blockquote", value=block, children=[], props=None)
            root.children.append(new_block)
        elif block_type.startswith(block_type_heading):
            new_block = HTMLNode(tag="h" + block_type[-1], value=block, children=[], props=None)
            root.children.append(new_block)
        elif block_type == block_type_paragraph:
            new_block = HTMLNode(tag="p", value=block, children=[], props=None)
            root.children.append(new_block)
        else:
            raise NotImplementedError(f"Unknown block type: {block_type}")
        
    