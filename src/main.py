from nodeutils import *
from textnode import TextNode

# original_nodes = [TextNode("This is a sentence with a *bold phrase* in it.", "text")]
# split_nodes = split_nodes_delimiter(original_nodes, "*", "bold")
# print(split_nodes)

test_node_images = [
    TextNode(
        "This is a text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        "text",
    )
]
# test_node_images = [TextNode("This is a text with a link ![to boot dev](https://www.boot.dev) and ...", "text")]

split_nodes = split_nodes_image(test_node_images)

for node in split_nodes:
    print(f"Text: {node.text}, Type: {node.text_type}, URL: {node.url}")

# import re

# text = "This is a text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
# text = "and ..."
# delimiter = "![to boot dev](https://www.boot.dev)"
# result = re.split("(" + re.escape(delimiter) + ")", text)

# print(result)
