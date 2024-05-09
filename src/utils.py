from leafnode import LeafNode
from textnode import TextNode
import re

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

def split_nodes_delimeter(old_nodes, delim, text_type):
    text_type_code, text_type_text, text_type_image, text_type_bold, text_type_italic, text_type_link = "code", "text", "image", "bold", "italic", "link"
    def splitter(node):
        fd = re.escape(f"{delim}")
        delim_match = re.findall(rf'{fd}(.*?){fd}', node.text)
        text = [phr for phr in node.text.split(delim) if phr != ""]
        if len(delim_match) > 0:
            return [TextNode(phr, text_type) if phr in delim_match else TextNode(phr, text_type_text) for phr in text]
        else:
            raise Exception("Not valid Markdown syntax")
    out = [splitter(node) if node.text_type == text_type_text else [node] for node in old_nodes]
    return out

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

