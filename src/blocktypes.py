from enum import Enum
import re

class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    if check_heading(block) == True:
        block_type = BlockType.HEAD
    elif block.startswith("```") and block.endswith("```"):
        block_type = BlockType.CODE
    elif check_line(block, ">") == True:
        block_type = BlockType.QUOTE
    elif check_line(block, "- ") == True:
        block_type = BlockType.ULIST
    elif check_olist(block) == True:
        block_type = BlockType.OLIST
    else:
        block_type = BlockType.PARA
    

    return block_type


# this is a helper function to check if a block is a heading
def check_heading(block):
    pattern = r"^(#{1,6}) "
    return bool(re.match(pattern, block))


# this is a helper function to check lines
def check_line(block, chars):
    lines = block.splitlines()
    for line in lines:
        if not line.startswith(chars):
            return False

    return True

# this is a helper function to check for ordered lists
def check_olist(block):
    lines = block.splitlines()
    line_count = 1
    for line in lines:
        if not line.startswith(str(line_count) + ". "):
            return False
        else:
            line_count += 1

    return True