from textnode import TextNode
from htmlnode import HtmlNode
from parentnode import ParentNode
from leafnode import LeafNode

nested_parent = ParentNode("p",
                          [LeafNode("b", "Bold text"),
                           LeafNode(None, "Normal text"),
                           LeafNode("i", "italic text"),
                           LeafNode(None, "Normal text"),],
                           )
sub_node = ParentNode("div", [LeafNode("b", "should be on same level as nested parent"), nested_parent])
main_node = ParentNode("doc",[LeafNode("title", "this is a title"), sub_node])

t = main_node.to_html()
print(t)
