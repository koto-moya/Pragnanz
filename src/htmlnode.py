class HtmlNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        print(f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})")
    
    def __eq__(self, node):
        if self.tag == node.tag and self.value == node.value and self.children == node.children and self.props == node.props:
            return True

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            return "".join([f" {k}=\"{v}\"" for k,v in self.props.items()])
        else:
            return ""
