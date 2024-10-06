import re

from textnode import TextNode
from leafnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:

    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == text_type_image:
        return LeafNode(
            "img", value="", props={"src": text_node.url, "alt": text_node.text}
        )
    else:
        raise NotImplementedError(f"Unknown text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str):

    new_nodes = []
    escaped_delimiter = re.escape(delimiter)
    regex_pattern = rf"({escaped_delimiter}(.*?){escaped_delimiter})"
    for node in old_nodes:
        split_texts = node.text.split(delimiter)
        matches = re.findall(regex_pattern, node.text)
        isolate_matches = [match[1] for match in matches]

        for text in split_texts:
            if text in isolate_matches:
                new_nodes.append(TextNode(text, text_type, url=node.url))
            else:
                new_nodes.append(TextNode(text, node.text_type, url=node.url))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    regex_pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex_pattern, text)

    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    regex_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex_pattern, text)

    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes = []
    for node in old_nodes:
        delimiter = r"(!\[.*?\]\(.*?\))"
        split_text = re.split(delimiter, node.text)

        for text in split_text:
            if text == "":
                continue
            if text.startswith("!"):
                image_text, image_url = extract_markdown_images(text)[0]
                new_nodes.append(TextNode(image_text, text_type_image, url=image_url))
            else:
                new_nodes.append(TextNode(text, node.text_type, url=node.url))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes = []
    for node in old_nodes:
        delimiter = r"(\[.*?\]\(.*?\))"
        split_text = re.split(delimiter, node.text)

        for text in split_text:
            if text == "":
                continue
            if text.startswith("["):
                link_text, link_url = extract_markdown_links(text)[0]
                new_nodes.append(TextNode(link_text, text_type_link, url=link_url))
            else:
                new_nodes.append(TextNode(text, node.text_type, url=node.url))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:

    original_text_node = [TextNode(text, text_type_text)]
    parsed_bold_text = split_nodes_delimiter(original_text_node, "**", text_type_bold)
    parsed_italic_text = split_nodes_delimiter(parsed_bold_text, "*", text_type_italic)
    parsed_code_text = split_nodes_delimiter(parsed_italic_text, "`", text_type_code)
    parsed_image_links = split_nodes_image(parsed_code_text)
    parsed_regular_links = split_nodes_link(parsed_image_links)

    return parsed_regular_links
