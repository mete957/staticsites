from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode

def text_node_to_html_node(text_node):
 
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        # ITALIC tipi: "i" tag'i, value metni.
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        # CODE tipi: "code" tag'i, value metni.
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
         if text_node.url is None:
              raise ValueError("Link TextNode must have a url")
         return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
         if text_node.url is None or text_node.text is None:
              raise ValueError("Image TextNode must have both url and text for alt attribute")
         return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unhandled text node type: {text_node.text_type}")
