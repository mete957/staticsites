import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    

    def test_eq(self):
        # Test case 1: Two identical nodes should be equal
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false_different_text(self):
        # Test case 2: Nodes with different text should not be equal
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is different text", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_false_different_type(self):
        # Test case 3: Nodes with different text types should not be equal
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false_different_url(self):
        # Test case 4: Nodes with different URLs should not be equal
        node = TextNode("This is a link node", TextType.LINK, "https://www.example.com")
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_eq_true_url(self):
        # Test case 5: Identical nodes with the same URL should be equal
        node = TextNode("This is a link node", TextType.LINK, "https://www.example.com")
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.example.com")
        self.assertEqual(node, node2)

    def test_eq_false_url_none(self):
        # Test case 6: Node with URL vs node with None URL should not be equal
        node = TextNode("This is a text node", TextType.TEXT, "https://www.example.com")
        node2 = TextNode("This is a text node", TextType.TEXT, None)
        self.assertNotEqual(node, node2)

    def test_eq_true_url_none(self):
        # Test case 7: Two nodes with None URL should be equal if other properties match
        node = TextNode("This is a text node", TextType.TEXT, None)
        node2 = TextNode("This is a text node", TextType.TEXT, None)
        self.assertEqual(node, node2)

    def test_eq_false_different_object_type(self):
        # Test case 8: Comparing a TextNode to a different type of object
        node = TextNode("This is a text node", TextType.TEXT)
        not_a_node = "Just a string"
        self.assertNotEqual(node, not_a_node)


# This block allows you to run the tests directly from the script
if __name__ == "__main__":
    unittest.main()

