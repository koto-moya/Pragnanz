from htmlnode import HtmlNode

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props = props)
        
    def to_html(self):
        if not self.tag:
            raise ValueError("No tag provided in parentnode")
        if not self.children:
            raise ValueError("No children in this parentnode")
        html_children = "".join([c.to_html() for c in self.children])
        
        return f"<{self.tag}{self.props_to_html()}>{html_children}</{self.tag}>"

