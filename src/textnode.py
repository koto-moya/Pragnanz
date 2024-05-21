class TextNode():
    def __init__(self, text, text_type: str, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, txtNode):
        if self.text == txtNode.text and self.text_type == txtNode.text_type and self.url == txtNode.url:
            return True
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
