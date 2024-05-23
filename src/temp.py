from utils import markdown_to_block, block_to_nodes, textnode_to_htmlnode, block_to_block_type
from textnode import TextNode
from md_to_html import blocked_leafs_to_html
import re

with open("/home/koto/build/hyde/content/index.md", "r") as file:
    markdown = file.read()
#blocks = markdown_to_block(markdown)
#blocked_nodes = [(block_to_nodes(block, block_to_block_type(block)), block_to_block_type(block)) for block in blocks]
#leaf_nodes = [(block_type, [textnode_to_htmlnode(node) for node in blocks]) for blocks, block_type in blocked_nodes]
#html = blocked_leafs_to_html(leaf_nodes)
html = 
print(html)
