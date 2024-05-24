from leafnode import LeafNode
from textnode import TextNode
import re

def validate_ordered_list(block):
    lines = block.split("\n")
    for line in lines:
        if not re.match(r"^\d+\.", line):
            return False
    for i, line in enumerate(lines):
            num = int(line.split(".")[0])
            if num != i+1:
                return False
    return True

def block_to_block_type(block: str):
    heading = re.findall(r"^#{1,6} ", block)
    code_block = re.findall(r"^`{3}.*`{3}$", block, re.DOTALL) # to compensate for new lines started directly after the ```
    quote = re.fullmatch(r"(>[^\n]*(?:\n>[^\n]*)*)$", block)
    unord_list = re.fullmatch(r"^(?:[\*\-] .*(?:\n[\*\-] .*)*)$", block)
    ord_list =  validate_ordered_list(block)
    if heading:
        return "heading"
    if code_block:
        return "code"
    if quote:
        return "quote"
    if unord_list:
        return "unordered list"
    if ord_list:
        return "ordered list"
    else:
        return "paragraph"

def markdown_to_block(markdown):
    split = markdown.split("\n\n")
    return [phr.lstrip("\n").rstrip("\n").lstrip(" ").rstrip(" ") for phr in split if phr != ""]


def textnode_to_htmlnode(text_node):
    lu = {"text":{"args":("",text_node.text), "props":None},
            "bold":{"args":("b",text_node.text), "props":None},
            "italic":{"args":("i",text_node.text), "props":None},
            "code":{"args":("code",text_node.text), "props":None},
            "link":{"args":("a",text_node.text), "props":{"href":text_node.url}},
            "image":{"args":("img",""), "props":{"src":text_node.url, "alt":text_node.text}}}

    try:
        ak = lu[text_node.text_type]
        return LeafNode(ak["args"][0],ak["args"][1], props=ak["props"])
    except:
        raise Exception("not a valid text type")

def get_lnk_args(i):
    if i[0] == "[" and i[-1] == ")":
        text = re.findall(r"\[([^\]]*)\]", i)
        link =  re.findall(r"\((.*?)\)", i)
        if text and link:
            return (text[0], link[0])
        else:
            return i
    else:
        return i

def get_img_args(i):
    if i[0] == "!":
        text = re.findall(r"\[([^\]]*)\]", i)
        link =  re.findall(r"\((.*?)\)", i)
        if text and link:
            return (text[0], link[0])
        else:
            return i
    else:
        return i

def split_logic(node, split_criteria, text_type) -> list:
        match = re.findall(split_criteria, node.text)
        if match:
            split = [phr for phr in re.split(split_criteria, node.text) if phr]
            return [TextNode(phr, text_type) if phr in match else TextNode(phr,"text") for phr in split]
        else:
            return [node]

def splitter(nodes: list, split_criteria, text_type) -> list:
    return sum([split_logic(node, split_criteria, text_type) for node in nodes], [])

def text_to_textnodes(input_block, block_type=None) -> list:
    # block -> [textnode]
    if block_type == "code":
        return [TextNode(input_block, "text")]
    else:
        textnode = [TextNode(input_block, "text")]
        # Bold pass
        out = splitter(textnode,r'\*\*([^*]+)\*\*',"bold")
        # italic pass
        out = splitter(out, r'\*([^*]+)\*', "italic")
        # code pass
        out = splitter(out, r'\`(.*?)\`', "code")
        # image pass
        out = splitter(out, r"(!\[[^\]]*\]\([^)]*\))", "image")
        # link pass
        out = splitter(out, r"(?<!\!)(\[[^\]]*\]\([^)]*\))", "link")
        return out

def clean_image_and_link(node) -> TextNode:
    if node.text_type == "link":
        link_args = get_lnk_args(node.text)
        return TextNode(link_args[0], node.text_type,link_args[1])
    elif node.text_type == "image":
        image_args = get_img_args(node.text)
        return TextNode(image_args[0], node.text_type, image_args[1])
    else:
        return node

def block_to_nodes(input_block, block_type=None) -> list:
    nodes = text_to_textnodes(input_block, block_type)
    return [clean_image_and_link(node) for node in nodes]
