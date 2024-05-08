from htmlnode import HtmlNode
from textnode import TextNode
from leafnode import LeafNode
from parentnode import ParentNode
from utils import textnode_to_htmlnode
import unittest

class TestTexttoHtml(unittest.TestCase):
    def test_texttohtml_text(self):
        tn = textnode_to_htmlnode(TextNode("test text","text"))
        self.assertEqual(tn, LeafNode("", "test text"))
    def test_texttohtml_bold(self):
        tn = textnode_to_htmlnode(TextNode("bolded","bold"))
        self.assertEqual(tn, LeafNode("b", "bolded"))
    def test_texttohtml_italic(self):
        tn = textnode_to_htmlnode(TextNode("Italics","italic"))
        self.assertEqual(tn, LeafNode("i", "Italics"))
    def test_texttohtml_code(self):
        tn = textnode_to_htmlnode(TextNode("code snippet","code"))
        self.assertEqual(tn, LeafNode("code", "code snippet"))
    def test_texttohtml_link(self):
        tn = textnode_to_htmlnode(TextNode("anchor text","link", "www.t.com"))
        self.assertEqual(tn, LeafNode("a", "anchor text", props={"href": "www.t.com"}))
    def test_texttohtml_image(self):
        tn = textnode_to_htmlnode(TextNode("alt text","image", "img.png"))
        self.assertEqual(tn, LeafNode("img", "", props={"src":"img.png", "alt":"alt text"}))

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"key1":"value1", "key2":"value2"}
        manual = "".join([f" {k}=\"{v}\"" for k,v in props.items()])
        func = HtmlNode(props = props)
        self.assertEqual(manual, func.props_to_html())

class testTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("v1", "v2", "v3")
        node2 = TextNode("v1", "v2", "v3")
        self.assertEqual(node1, node2)
    
    def test_eq2(self):
        node1 = TextNode("v1", "v2", None)
        node2 = TextNode("v1", "v2", None)
        self.assertEqual(node1, node2)
    
    def test_eq3(self):
        node1 = TextNode("v1", "v2", None)
        node2 = TextNode("v1", "v2","v3")
        self.assertNotEqual(node1, node2)

    def test_eq4(self):
        node1 = TextNode("v1", "v9", "v3")
        node2 = TextNode("v1", "v2","v3")
        self.assertNotEqual(node1, node2)

    def test_eq5(self):
        node1 = TextNode("v0", "v2", "v3")
        node2 = TextNode("v1", "v2","v3")
        self.assertNotEqual(node1, node2)

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_props(self):
        leaf = LeafNode("p","text")
        html = leaf.to_html()
        self.assertEqual(html, "<p>text</p>")

    def test_to_html_props(self):
        leaf = LeafNode("a","link", {"href":"https://www.google.com"})
        html = leaf.to_html()
        self.assertEqual(html, "<a href=\"https://www.google.com\">link</a>")

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode("p",
                          [LeafNode("b", "Bold text"),
                           LeafNode(None, "Normal text"),
                           LeafNode("i", "italic text"),
                           LeafNode(None, "Normal text"),],
                           )
        test_out = node.to_html()
        self.assertEqual(test_out, "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html2(self):
        nested_parent = ParentNode("p",
                          [LeafNode("b", "Bold text"),
                           LeafNode(None, "Normal text"),
                           LeafNode("i", "italic text"),
                           LeafNode(None, "Normal text"),],
                           )
        node = ParentNode("div", [LeafNode("p", "test"), nested_parent],)
        test_out = node.to_html()
        self.assertEqual(test_out, "<div><p>test</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>")

