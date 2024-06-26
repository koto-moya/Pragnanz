from utils import markdown_to_block, block_to_block_type, block_to_nodes, textnode_to_htmlnode
from textnode import TextNode
from parentnode import ParentNode
from leafnode import LeafNode
import re
def markdown_to_leafnodes(markdown):
    blocks = markdown_to_block(markdown)
    blocked_nodes = [block_to_nodes(block, block_to_block_type(block)) for block in blocks]
    return [(block_type, [textnode_to_htmlnode(node) for node in blocks]) for blocks, block_type in blocked_nodes]

def quote_to_html(leaf_group):
    leaf_group = [LeafNode(leaf.tag,re.sub(r"> ", "", leaf.value)) for leaf in leaf_group]
    return ParentNode("blockquote", leaf_group).to_html()

def list_to_html(leaf_group, list_type): 
    values = "".join([leaf.value if leaf.tag == "" else leaf.to_html() for leaf in leaf_group])
    urls = {}
    def replace_url(match):
        placeholder = f"URL{len(urls)}"
        urls[placeholder] = match.group(0)
        return placeholder
    
    text = re.sub(r'https?://[\S]+', replace_url, values)
    
    # Perform replacements on the non-URL text
    text = re.sub(r'^\d+\.\s', "", text, flags=re.MULTILINE)
    text = re.sub(r'[-*]', "", text, flags=re.MULTILINE)
    
    # Restore URLs from placeholders
    for placeholder, url in urls.items():
        text = text.replace(placeholder, url)
    split = text.split("\n") 
    li_leafs = [LeafNode("li", line) for line in split]
    return ParentNode(f"{list_type}",li_leafs).to_html()

def code_to_html(leaf_group):
    leaf_group = [LeafNode(leaf.tag,re.sub(r"^```\n|```$", "", leaf.value)) for leaf in leaf_group]
    return ParentNode("pre", [ParentNode("code", leaf_group)]).to_html()

def heading_to_html(leaf_group):
    joined = "".join([leaf.value if leaf.tag == "" else leaf.to_html() for leaf in leaf_group])
    header_value = LeafNode("",joined.lstrip("#").lstrip(" "))
    split = joined.split(" ")
    h_count = split[0].count("#")
    if h_count > 6:
        h_count=6
    return ParentNode(f"h{h_count}", [header_value]).to_html()

def paragraph_to_html(leaf_group):
    return ParentNode("p", leaf_group).to_html()

def blocked_leafs_to_html(zipped_leafs):
    parent_nodes = []
    for block_type, leaf_group in zipped_leafs:
        if block_type == "quote":
            parent_nodes.append(quote_to_html(leaf_group))
        elif block_type == "unordered list":
            parent_nodes.append(list_to_html(leaf_group, "ul"))
        elif block_type == "ordered list":
            parent_nodes.append(list_to_html(leaf_group, "ol"))
        elif block_type == "code":
            parent_nodes.append(code_to_html(leaf_group))
        elif block_type == "heading":
            parent_nodes.append(heading_to_html(leaf_group))
        elif block_type == "paragraph":
            parent_nodes.append(paragraph_to_html(leaf_group))
        else:
            raise Exception("Invalid Block Type")
    return f'<div>{"".join(parent_nodes)}</div>'

def markdown_to_html(text):
    return blocked_leafs_to_html(markdown_to_leafnodes(text))

