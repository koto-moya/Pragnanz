from htmlnode import HtmlNode


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag == "img":
            props = self.props_to_html()
            return f"<{self.tag}{props}>"
        else:
            if not self.value:
                raise ValueError("No values in leafnode")
            if not self.tag:
                return str(self.value)        
            if self.props:
                props = self.props_to_html()
                return f"<{self.tag}{props}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
