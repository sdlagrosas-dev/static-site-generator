import unittest

from mdblockutils import *


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        markdown_text = "This is a sentence with a ![rickroll](https://example.com/image.png) and another ![troll](https://example.com/troll.png)\n\nThis is a sentence with a [link](https://example.com) and another [troll](https://example.com/troll)\n\nLastly, this is a sentence with a **bold** and an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        blocks = markdown_to_blocks(markdown_text)

        self.assertEqual(
            blocks[0],
            "This is a sentence with a ![rickroll](https://example.com/image.png) and another ![troll](https://example.com/troll.png)",
        )
        self.assertEqual(
            blocks[1],
            "This is a sentence with a [link](https://example.com) and another [troll](https://example.com/troll)",
        )
        self.assertEqual(
            blocks[2],
            "Lastly, this is a sentence with a **bold** and an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
        )

    def test_markdown_to_blocks_with_empty_lines(self):
        markdown_text = """This is a sentence with a ![rickroll](https://example.com/image.png) and another ![troll](https://example.com/troll.png)
        
        This is a sentence with a [link](https://example.com) and another [troll](https://example.com/troll)
        
        
        Lastly, this is a sentence with a **bold** and an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"""

        blocks = markdown_to_blocks(markdown_text)

        self.assertEqual(
            blocks[0],
            "This is a sentence with a ![rickroll](https://example.com/image.png) and another ![troll](https://example.com/troll.png)",
        )
        self.assertEqual(
            blocks[1],
            "This is a sentence with a [link](https://example.com) and another [troll](https://example.com/troll)",
        )
        self.assertEqual(
            blocks[2],
            "Lastly, this is a sentence with a **bold** and an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
        )

    def test_markdown_to_blocks_with_trailing_newlines(self):
        markdown_text = """
        
        
        This is a sentence with a ![rickroll](https://example.com/image.png) and another ![troll](https://example.com/troll.png)
        
        This is a sentence with a [link](https://example.com) and another [troll](https://example.com/troll)
        

        """
        blocks = markdown_to_blocks(markdown_text)

        self.assertEqual(
            blocks[0],
            "This is a sentence with a ![rickroll](https://example.com/image.png) and another ![troll](https://example.com/troll.png)",
        )
        self.assertEqual(
            blocks[1],
            "This is a sentence with a [link](https://example.com) and another [troll](https://example.com/troll)",
        )
        self.assertEqual(len(blocks), 2)


class TestBlockToBlockType(unittest.TestCase):

    def test_block_to_block_type(self):
        block = "This is a normal paragraph"

        block_type = block_to_block_type(block)

        self.assertEqual(block_type, block_type_paragraph)

    def test_block_to_block_type_header(self):
        block_1 = "# This is a header"
        block_2 = "## This is another header"
        block_3 = "### This is yet another header"
        block_4 = "#### This is yet another header"
        block_5 = "##### This is yet another header"
        block_6 = "###### This is yet another header"

        block_1_type = block_to_block_type(block_1)
        block_2_type = block_to_block_type(block_2)
        block_3_type = block_to_block_type(block_3)
        block_4_type = block_to_block_type(block_4)
        block_5_type = block_to_block_type(block_5)
        block_6_type = block_to_block_type(block_6)

        self.assertEqual(block_1_type, block_type_heading)
        self.assertEqual(block_2_type, block_type_heading)
        self.assertEqual(block_3_type, block_type_heading)
        self.assertEqual(block_4_type, block_type_heading)
        self.assertEqual(block_5_type, block_type_heading)
        self.assertEqual(block_6_type, block_type_heading)

    def test_block_to_block_type_header_7(self):
        block_7 = "####### This is an invalid header"

        block_type_7 = block_to_block_type(block_7)

        self.assertEqual(block_type_7, block_type_paragraph)

    def test_block_to_block_type_header_invalid(self):
        block = "##This is not a valid header"

        block_type = block_to_block_type(block)

        self.assertEqual(block_type, block_type_paragraph)



if __name__ == "__main__":
    unittest.main()
