from src.utils import markdown_to_block, block_to_block_type, text_to_textnodes, textnode_to_htmlnode
from src.textnode import TextNode
from src.parentnode import ParentNode
from src.leafnode import LeafNode

with open("markdown.md", "r") as file:
    text = file.read()
blocks = markdown_to_block(text)
text_nodes = [text_to_textnodes(block) for block in blocks]
block_types = [block_to_block_type(block) for block in blocks]
leaf_nodes = []
for groups in text_nodes:
    leaf_nodes.append([textnode_to_htmlnode(node) for node in groups])

zipped_leafs = zip(block_types, leaf_nodes) 
#for i in zipped_leafs:
 #   print(i)
parent_nodes = []
for block_type, leaf_group in zipped_leafs:
    if block_type == "quote":
        parent_nodes.append(ParentNode("blockquote", leaf_group).to_html())
    elif block_type == "unordered list":
        values = "".join([leaf.value if leaf.tag == "" else leaf.to_html() for leaf in leaf_group])
        split = values.split("\n")
        li_leafs = [LeafNode("li", line) for line in split]
        parent_nodes.append(ParentNode("ul",li_leafs).to_html())
    elif block_type == "ordered list":
        values = "".join([leaf.value if leaf.tag == "" else leaf.to_html() for leaf in leaf_group])
        split = values.split("\n")
        li_leafs = [LeafNode("li", line) for line in split]
        parent_nodes.append(ParentNode("ol",li_leafs).to_html())
    elif block_type == "code":
        parent_nodes.append(ParentNode("pre", [ParentNode("code", leaf_group)]).to_html())
    elif block_type == "heading":
        joined = "".join([leaf.value if leaf.tag == "" else leaf.to_html() for leaf in leaf_group])
        header_value = LeafNode("",joined.lstrip("#").lstrip(" "))
        split = joined.split(" ")
        h_count = split[0].count("#")
        if h_count > 6:
            h_count=6
        parent_nodes.append(ParentNode(f"h{h_count}", [header_value]).to_html())
    elif block_type == "paragraph":
        parent_nodes.append(ParentNode("p", leaf_group).to_html())
    else:
        raise Exception("Invalid Block Type")



print(f"<div>{"".join(parent_nodes)}</div>")
