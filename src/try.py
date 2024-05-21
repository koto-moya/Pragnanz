from utils import block_to_block_type
from textnode import TextNode

test_string = "1. test\n*. test2"
out = block_to_block_type(test_string)
print(out)
