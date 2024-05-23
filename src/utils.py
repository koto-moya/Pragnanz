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

def text_to_textnodes(text):
    text_node = TextNode(text,"text")
    print("***New Block***")
    bold = split_nodes_delimiter([text_node], "**", "bold")
    print(f"bolded pass:\n{bold}\nNumber of nodes: {len(bold)}\n")
    italic = split_nodes_delimiter(bold, "*", "italic")
    print(f"italic pass:\n{italic}\nNumber of nodes: {len(italic)}\n")
    code = split_nodes_delimiter(italic, "`", "code")
    print(f"code pass:\n{code}\nNumber of nodes: {len(code)}\n")
    image = split_nodes_delimiter(code,r"(!\[[^\]]*\]\([^)]*\))", "image")
    print(f"image pass:\n{image}\nNumber of nodes: {len(image)}\n")
    link = split_nodes_delimiter(image, r"(?<!\!)(\[[^\]]*\]\([^)]*\))", "link")
    print(f"link pass:\n{link}\nNumber of nodes: {len(link)}\n\n")
    return link

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

def splitter(node, delim, text_type):
    if text_type == "link":
        match = re.findall(delim, node.text)
        text = [get_lnk_args(phr) for phr in re.split(delim, node.text) if phr]
        return [TextNode(phr[0], text_type, phr[1]) if f"[{phr[0]}]({phr[1]})" in match else TextNode(phr, "text") for phr in text]
    elif text_type == "image":
        match = re.findall(delim, node.text)
        text = [get_img_args(phr) for phr in re.split(delim, node.text) if phr]
        return [TextNode(phr[0], text_type, phr[1]) if f"![{phr[0]}]({phr[1]})" in match else TextNode(phr, "text") for phr in text]
    else:
        if delim == "`":
            delim_match = re.findall(r'(?<!`)`([^`]+)`(?!`)', node.text)
            text = [phr for phr in re.split(r'(?<!`)`([^`]+)`(?!`)', node.text) if phr != ""]
        elif delim == "*": 
            delim_match = re.findall(r'\*([^*]+)\*', node.text) 
            text = [phr for phr in re.split(r'\*([^*]+)\*', node.text) if phr != ""] 
        elif delim == "**": 
            delim_match = re.findall(r'\*\*([^*]+)\*\*', node.text) 
            text = [phr for phr in re.split(r'\*\*([^*]+)\*\*', node.text) if phr != ""]
        else:
            fd = re.escape(f"{delim}")
            delim_match = re.findall(rf'{fd}(.*?){fd}', node.text)
            text = [phr for phr in node.text.split(delim) if phr != ""]
        return [TextNode(phr, text_type) if phr in delim_match else TextNode(phr, "text") for phr in text]

def split_nodes_delimiter(old_nodes, delim, text_type):
    out = [splitter(node, delim, text_type) if node.text_type == "text" else [node] for node in old_nodes]
    return sum(out, [])
