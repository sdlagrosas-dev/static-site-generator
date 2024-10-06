import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_no_children(self):
        node = LeafNode("p", "This is a text node")
        self.assertEqual(node.children, None)

    def test_repr(self):
        node = LeafNode("p", "This is a text node")
        self.assertEqual(repr(node), "HTMLNode(p, This is a text node, None, None)")

    def test_to_html(self):
        node = LeafNode("p", "This is a text node")
        self.assertEqual(node.to_html(), f"<p>This is a text node</p>")

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
