from utils import split_nodes_delimiter
from textnode import TextNode
import re
text  = "text"
italic = "italic"
def get_lnk_args(i):
    print(i)
    if i[0] == "[" and i[-1] == ")":
        text = re.findall(r"\[([^\]]*)\]", i)
        link =  re.findall(r"\((.*?)\)", i)
        if text and link:
            return (text[0], link[0])
        else:
            return i
    else:
        return i 

nodes = [TextNode("In the annals of fantasy literature and the broader realm of creative world-building, few sagas can rival the intricate tapestry woven by J.R.R. Tolkien in ", text, None), 
        TextNode("The Lord of the Rings", italic, None), 
        TextNode(". You can find the [wiki here](https://lotr.fandom.com/wiki/Main_Page).", text, None)]
test =  []
for node in nodes:
    match = re.findall(r"(?<!\!)(\[[^\]]*\]\([^)]*\))", node.text)
    split = re.split(r"(?<!\!)(\[[^\]]*\]\([^)]*\))", node.text) 
    test.append(get_lnk_args(split))
    print(f"Match:\n{match}")
    print(f"Split:\n{split}")
#test = split_nodes_delimiter(nodes, r"(?<!\!)(\[[^\]]*\]\([^)]*\))", "link")
print(f"\n\n\n{test}")
