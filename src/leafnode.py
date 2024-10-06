from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Value cannot be None")
        if self.tag is None:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"
