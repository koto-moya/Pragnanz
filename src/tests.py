from src.htmlnode import HtmlNode
from src.textnode import TextNode
from src.leafnode import LeafNode
from src.parentnode import ParentNode
from src.utils import textnode_to_htmlnode, split_nodes_delimeter, text_to_textnodes, markdown_to_block, block_to_block_type
import unittest

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "### test"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "heading")

    def test_code(self):
        block = "``` code # test ```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "code")

    def test_quote(self):
        block = ">test\n>quote\n>line"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "quote")
    
    def test_unordered_list(self):
        block = "* this\n* is\n- a\n* test"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "unordered list")

    def test_ordered_list(self):
        block = "1. this\n2. is\n3. a\n4. test"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "ordered list")

    def test_paragraph1(self):
        block = "1. test\nB. lines"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_paragraph2(self):
        block = "##test"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_paragraph3(self):
        block = ">test\n<line"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

class TestMarkdownToBlockd(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = '''This is **text** with an *italic* word and a\n\n`code`\n*test*'''
        block = markdown_to_block(markdown)
        self.assertEqual(block, ["This is **text** with an *italic* word and a", "`code`\n*test*"]) 
    def test_markdown_to_blocks2(self):
        markdown = '''This is **text** with an *italic* word and a\n\n\n`code`\n*test*'''
        block = markdown_to_block(markdown)
        self.assertEqual(block, ["This is **text** with an *italic* word and a", "`code`\n*test*"])

class TestTextToNode(unittest.TestCase):
    def test_text_to_textnode(self):
        text = "this is a text string with **bolded** words, *italics*, and some `code snippets`.  Here is an image to better explain ![image text](image.jpg).  Also, for more information follow this link: [link_title](https://www.google.com)"
        textnode = text_to_textnodes(text)
        self.assertEqual(textnode, [TextNode("this is a text string with ", "text", None), TextNode("bolded", "bold", None), TextNode(" words, ", "text", None), TextNode("italics", "italic", None), TextNode(", and some ", "text", None), TextNode("code snippets", "code", None), TextNode(".  Here is an image to better explain ", "text", None), TextNode("image text", "image", "image.jpg"), TextNode(".  Also, for more information follow this link: ", "text", None), TextNode("link_title", "link", "https://www.google.com")])

class TestSplitNodesDelim(unittest.TestCase):
    def test_splitnode_delim1(self):
        nodes = [TextNode("This is a test with a **bolded** word", "text")]
        sn = split_nodes_delimeter(nodes, "**", "bold")
        self.assertEqual(sn, [TextNode("This is a test with a ", "text"), TextNode("bolded", "bold"), TextNode(" word", "text")]) 
    def test_splitnode_delim2(self):
        nodes = [TextNode("This is a test with two **bold** words like **bolded**", "text")]
        sn = split_nodes_delimeter(nodes, "**", "bold")
        self.assertEqual(sn, [TextNode("This is a test with two ", "text"), TextNode("bold", "bold"), TextNode(" words like ", "text"), TextNode("bolded", "bold")])
    def test_splitnode_delim3(self):
        nodes = [TextNode("This is a for two or more nodes with `code` ", "text"), TextNode("More `code`", "text")]
        sn = split_nodes_delimeter(nodes, "`", "code")
        self.assertEqual(sn, [TextNode("This is a for two or more nodes with ", "text"), TextNode("code", "code"), TextNode(" ", "text"),TextNode("More ", "text"), TextNode("code", "code")])
    def test_splitnode_delim4(self):
        nodes = [TextNode("This is a test with two *italic* words like *italics*", "text")]
        sn = split_nodes_delimeter(nodes, "*", "italic")
        self.assertEqual(sn, [TextNode("This is a test with two ", "text"), TextNode("italic", "italic"), TextNode(" words like ", "text"), TextNode("italics", "italic")])

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

