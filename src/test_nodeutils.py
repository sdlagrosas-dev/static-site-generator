import unittest

from textnode import TextNode
from leafnode import LeafNode
from nodeutils import *


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node(self):
        text_node = TextNode("normal text", "text")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "normal text")

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("bold text", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "bold text")
        self.assertEqual(html_node.tag, "b")

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("link text", "link", "https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "link text")
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("image text", "image", "https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "https://example.com/image.png")
        self.assertEqual(html_node.props["alt"], "image text")

    def test_text_node_to_html_node_invalid(self):
        text_node = TextNode("invalid text", "invalid")
        with self.assertRaises(NotImplementedError):
            text_node_to_html_node(text_node)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_italic(self):
        original_nodes = [
            TextNode("This is a sentence with a *italic phrase* in it.", "text")
        ]
        split_nodes = split_nodes_delimiter(original_nodes, "*", "italic")
        self.assertEqual(split_nodes[0].text, "This is a sentence with a ")
        self.assertEqual(split_nodes[1].text, "italic phrase")
        self.assertEqual(split_nodes[2].text, " in it.")
        self.assertEqual(split_nodes[1].text_type, "italic")

    def test_split_nodes_delimiter_code(self):
        original_nodes = [
            TextNode("This is a sentence with a `code phrase` in it.", "text")
        ]
        split_nodes = split_nodes_delimiter(original_nodes, "`", "code")
        self.assertEqual(split_nodes[0].text, "This is a sentence with a ")
        self.assertEqual(split_nodes[1].text, "code phrase")
        self.assertEqual(split_nodes[2].text, " in it.")
        self.assertEqual(split_nodes[1].text_type, "code")

    def test_split_nodes_delimiter_bold(self):
        original_nodes = [
            TextNode("This is a sentence with a **bold phrase** in it.", "text")
        ]
        split_nodes = split_nodes_delimiter(original_nodes, "**", "bold")
        self.assertEqual(split_nodes[0].text, "This is a sentence with a ")
        self.assertEqual(split_nodes[1].text, "bold phrase")
        self.assertEqual(split_nodes[2].text, " in it.")
        self.assertEqual(split_nodes[1].text_type, "bold")

    def test_split_nodes_delimiter_no_bold(self):
        original_nodes = [
            TextNode("This is a sentence without a delimited phrase in it.", "text")
        ]
        split_nodes = split_nodes_delimiter(original_nodes, "**", "bold")
        self.assertEqual(
            split_nodes[0].text, "This is a sentence without a delimited phrase in it."
        )

    def test_split_nodes_delimeter_bold_isolated(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        original_nodes = [TextNode(text, "text")]
        split_nodes = split_nodes_delimiter(original_nodes, "**", "bold")
        self.assertEqual(split_nodes[0].text, "This is ")
        self.assertEqual(split_nodes[1].text, "text")
        self.assertEqual(split_nodes[1].text_type, "bold")
        self.assertEqual(
            split_nodes[2].text,
            " with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        markdown_text = (
            "This is a sentence with a ![rickroll](https://example.com/image.png)"
        )
        images = extract_markdown_images(markdown_text)
        self.assertEqual(images, [("rickroll", "https://example.com/image.png")])

    def test_extract_markdown_images_multiple(self):
        markdown_text = "This is a sentence with a ![rickroll](https://example.com/image.png) and another ![troll](https://example.com/troll.png)"
        images = extract_markdown_images(markdown_text)
        self.assertEqual(
            images,
            [
                ("rickroll", "https://example.com/image.png"),
                ("troll", "https://example.com/troll.png"),
            ],
        )


class TestExtreactMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        markdown_text = "This is a sentence with a [link](https://example.com)"
        links = extract_markdown_links(markdown_text)
        self.assertEqual(links, [("link", "https://example.com")])

    def test_extract_markdown_links_multiple(self):
        markdown_text = "This is a sentence with a [link](https://example.com) and another [troll](https://example.com/troll)"
        links = extract_markdown_links(markdown_text)
        self.assertEqual(
            links,
            [("link", "https://example.com"), ("troll", "https://example.com/troll")],
        )


class TestSplitNodesImage(unittest.TestCase):

    def test_split_nodes_single_image(self):
        original_nodes = [
            TextNode(
                "This is a text with an image ![to boot dev](https://www.boot.dev/example.png)",
                "text",
            )
        ]
        split_nodes = split_nodes_image(original_nodes)
        self.assertEqual(split_nodes[0].text, "This is a text with an image ")
        self.assertEqual(split_nodes[1].text, "to boot dev")
        self.assertEqual(split_nodes[1].url, "https://www.boot.dev/example.png")

    def test_split_nodes_multiple_images(self):
        original_nodes = [
            TextNode(
                "This is a text with an image ![to boot dev](https://www.boot.dev/example.png) and ![to youtube](https://www.youtube.com/@bootdotdev/icon.png)",
                "text",
            )
        ]
        split_nodes = split_nodes_image(original_nodes)
        self.assertEqual(split_nodes[0].text, "This is a text with an image ")
        self.assertEqual(split_nodes[1].text, "to boot dev")
        self.assertEqual(split_nodes[2].text, " and ")
        self.assertEqual(split_nodes[3].text, "to youtube")
        self.assertEqual(split_nodes[1].url, "https://www.boot.dev/example.png")
        self.assertEqual(
            split_nodes[3].url, "https://www.youtube.com/@bootdotdev/icon.png"
        )

    def test_split_nodes_image_in_front(self):
        original_nodes = [
            TextNode("![to boot dev](https://www.boot.dev) is here!", "text")
        ]
        split_nodes = split_nodes_image(original_nodes)
        self.assertEqual(split_nodes[0].text, "to boot dev")
        self.assertEqual(split_nodes[0].url, "https://www.boot.dev")
        self.assertEqual(split_nodes[0].text_type, "image")
        self.assertEqual(split_nodes[1].text, " is here!")

    def test_split_nodes_no_images(self):
        original_nodes = [TextNode("This is a text with no images here", "text")]
        split_nodes = split_nodes_image(original_nodes)
        self.assertEqual(split_nodes, original_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        original_nodes = [
            TextNode(
                "This is a text with a link [to boot dev](https://www.boot.dev)", "text"
            )
        ]
        split_nodes = split_nodes_link(original_nodes)
        self.assertEqual(split_nodes[0].text, "This is a text with a link ")
        self.assertEqual(split_nodes[1].text, "to boot dev")
        self.assertEqual(split_nodes[1].text_type, "link")
        self.assertEqual(split_nodes[1].url, "https://www.boot.dev")

    def test_split_nodes_multiple_links(self):
        original_nodes = [
            TextNode(
                "This is a text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                "text",
            )
        ]
        split_nodes = split_nodes_link(original_nodes)
        self.assertEqual(split_nodes[0].text, "This is a text with a link ")
        self.assertEqual(split_nodes[1].text, "to boot dev")
        self.assertEqual(split_nodes[1].text_type, "link")
        self.assertEqual(split_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(split_nodes[2].text, " and ")
        self.assertEqual(split_nodes[3].text, "to youtube")
        self.assertEqual(split_nodes[3].text_type, "link")
        self.assertEqual(split_nodes[3].url, "https://www.youtube.com/@bootdotdev")

    def test_split_nodes_no_links(self):
        original_nodes = [TextNode("This is a text with no links here", "text")]
        split_nodes = split_nodes_link(original_nodes)
        self.assertEqual(split_nodes, original_nodes)


class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_text_nodes(self):
        text = """This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"""
        text_nodes = text_to_textnodes(text)
        self.assertEqual(text_nodes[0].text, "This is ")
        self.assertEqual(text_nodes[1].text, "text")
        self.assertEqual(text_nodes[1].text_type, "bold")
        self.assertEqual(text_nodes[2].text, " with an ")
        self.assertEqual(text_nodes[3].text, "italic")
        self.assertEqual(text_nodes[3].text_type, "italic")
        self.assertEqual(text_nodes[4].text, " word and a ")
        self.assertEqual(text_nodes[5].text, "code block")
        self.assertEqual(text_nodes[5].text_type, "code")
        self.assertEqual(text_nodes[6].text, " and an ")
        self.assertEqual(text_nodes[7].text, "obi wan image")
        self.assertEqual(text_nodes[7].text_type, "image")
        self.assertEqual(text_nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(text_nodes[8].text, " and a ")
        self.assertEqual(text_nodes[9].text, "link")
        self.assertEqual(text_nodes[9].text_type, "link")
        self.assertEqual(text_nodes[9].url, "https://boot.dev")

    def test_text_to_text_nodes_no_text(self):
        text = ""
        original_nodes = text_to_textnodes(text)
        self.assertEqual(original_nodes, [])


if __name__ == "__main__":
    unittest.main()
