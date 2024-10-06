from leafnode import LeafNode


class TextNode:

    def __init__(self, text: str, text_type: str, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode") -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    # def to_html_node(self) -> LeafNode:

    #     if self.text_type == "text":
    #         return LeafNode(None, self.text)
    #     elif self.text_type == "bold":
    #         return LeafNode("b", self.text)
    #     elif self.text_type == "italic":
    #         return LeafNode("i", self.text)
    #     elif self.text_type == "code":
    #         return LeafNode("code", self.text)
    #     elif self.text_type == "link":
    #         return LeafNode("a", self.text, props={"href": self.url})
    #     elif self.text_type == "image":
    #         return LeafNode("img", value=self.text, props={"src": self.url})
    #     else:
    #         raise NotImplementedError()
