import unittest
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from main import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    # ... (Daha önceki TestHTMLNode.props_to_html test metotları buraya gelecek)
    def test_props_to_html_basic(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p", props={})
        expected_output = ""
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_none(self):
        node = HTMLNode(tag="div") # props is None by default
        expected_output = ""
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(tag="input", props={"type": "text", "name": "username", "value": "test_user", "required": ""})
        output = node.props_to_html()
        self.assertIn(' type="text"', output)
        self.assertIn(' name="username"', output)
        self.assertIn(' value="test_user"', output)
        self.assertIn(' required=""', output)
        self.assertTrue(output.startswith(' '))
        self.assertEqual(len(output.split()), 4)

class TestLeafNode(unittest.TestCase):
    def test_to_html_paragraph(self):
        """
        Test case: LeafNode with a paragraph tag and value.
        Renders as <p>value</p>.
        """
        node = LeafNode("p", "This is a paragraph of text.")
        expected_html = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_link_with_props(self):
        """
        Test case: LeafNode with a link tag, value, and properties.
        Renders as <a href="...">value</a>.
        """
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_html = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_raw_text(self):
        """
        Test case: LeafNode with no tag (tag=None) and a value.
        Should return only the raw value string.
        """
        node = LeafNode(None, "This is just raw text.")
        expected_html = "This is just raw text."
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_value_none_raises_error(self):
        """
        Test case: LeafNode created (hypothetically) with value=None.
        Calling to_html() should raise a ValueError.
        (Constructor should prevent this state, but testing method robustness)
        """
        # Test etmek için, constructor'ı atlayıp value'yu None yapmamız gerekiyor.
        # Bu normal kullanımda olmaz ama metodun kendi kontrolünü test etmek için yapılır.
        node = LeafNode("p", "Geçerli bir değerle başla")
        node.value = None # value'yu None olarak değiştir

        # ValueError'ın yükseltildiğini kontrol et
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        # Yükseltilen hatanın mesajını da kontrol edebiliriz (isteğe bağlı)
        self.assertEqual(str(cm.exception), "Invalid HTML: LeafNode must have a value")

class TestParentNode(unittest.TestCase):
    # ... (ParentNode constructor'ı için yazdığınız test metotları buraya gelecek)
    def test_parentnode_init_valid(self):
         child1 = LeafNode("span", "İlk Çocuk Metni")
         child2 = LeafNode("b", "İkinci Çocuk Kalın Metin")
         children_list = [child1, child2]
         properties = {"class": "konteyner"}
         node = ParentNode("div", children_list, properties)
         self.assertEqual(node.tag, "div")
         self.assertIsNone(node.value)
         self.assertEqual(node.children, children_list)
         self.assertEqual(node.props, properties)

    def test_parentnode_init_no_tag_raises_error(self):
         child = LeafNode("span", "bir çocuk")
         children_list = [child]
         with self.assertRaises(ValueError) as cm:
             ParentNode(None, children_list)
         self.assertEqual(str(cm.exception), "ParentNode requires a tag")

    def test_parentnode_init_empty_tag_raises_error(self):
         child = LeafNode("span", "bir çocuk")
         children_list = [child]
         with self.assertRaises(ValueError) as cm:
             ParentNode("", children_list)
         self.assertEqual(str(cm.exception), "ParentNode requires a tag")

    def test_parentnode_init_no_children_raises_error(self):
         with self.assertRaises(ValueError) as cm:
             ParentNode("div", None)
         self.assertEqual(str(cm.exception), "ParentNode requires a non-empty list of children")

    def test_parentnode_init_empty_children_raises_error(self):
         with self.assertRaises(ValueError) as cm:
             ParentNode("div", [])
         self.assertEqual(str(cm.exception), "ParentNode requires a non-empty list of children")

    def test_parentnode_init_children_not_list_raises_error(self):
         with self.assertRaises(ValueError) as cm:
             ParentNode("div", "bu bir liste değil")
         self.assertEqual(str(cm.exception), "ParentNode requires a non-empty list of children")

    def test_parentnode_init_with_props(self):
         child = LeafNode("span", "çocuk")
         children_list = [child]
         properties = {"id": "ana-div", "data-test": "abc"}
         node = ParentNode("div", children_list, properties)
         self.assertEqual(node.tag, "div")
         self.assertIsNone(node.value)
         self.assertEqual(node.children, children_list)
         self.assertEqual(node.props, properties)


    # --- ParentNode.to_html() Metodu İçin Testler ---

    def test_to_html_with_children(self):
        """
        Test case: ParentNode with a single LeafNode child. (Örnek 1)
        Div tag'i ve span çocuğu olan basit bir senaryo.
        """
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        # Beklenen çıktı: <div><span>child</span></div>
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        """
        Test case: ParentNode with a ParentNode child, which has a LeafNode grandchild. (Örnek 2)
        İç içe geçmiş ParentNode'ları test eder (özyinelemeyi).
        """
        grandchild_node = LeafNode("b", "grandchild") # Torun: <b>grandchild</b>
        child_node = ParentNode("span", [grandchild_node]) # Çocuk: <span><b>grandchild</b></span>
        parent_node = ParentNode("div", [child_node]) # Ebeveyn: <div><span><b>grandchild</b></span></div>
        expected_html = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(parent_node.to_html(), expected_html)

    def test_to_html_multiple_children_no_props(self):
        """
        Test case: ParentNode with multiple LeafNode children of different types, no props on parent.
        Çocuklar arasında raw text (tag=None) olanları da içerir. (İstekteki örnek)
        """
        node = ParentNode(
            "p", # p tag'i olan parent
            [
                LeafNode("b", "Bold text"),      # Çocuk 1: <b>Bold text</b>
                LeafNode(None, "Normal text"), # Çocuk 2: Normal text (ham metin)
                LeafNode("i", "italic text"),    # Çocuk 3: <i>italic text</i>
                LeafNode(None, "Normal text"), # Çocuk 4: Normal text (ham metin)
            ],
        )
        # Beklenen çıktı: <p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_props_on_parent(self):
        """
        Test case: ParentNode with children and props on the parent tag.
        Ebeveyn tag'inin özelliklerinin (props) çıktıya dahil edildiğini doğrular.
        """
        child1 = LeafNode("span", "Span child")
        child2 = LeafNode("em", "Em child")
        children_list = [child1, child2]
        properties = {"id": "ebeveyn-id", "class": "ebeveyn-sinif"}
        parent_node = ParentNode("div", children_list, properties)
        # Beklenen çıktı: <div id="ebeveyn-id" class="ebeveyn-sinif"><span>Span child</span><em>Em child</em></div>
        # Not: Özelliklerin çıktıda görüneceği sıra Python 3.7 öncesi sürümlerde değişebilir.
        expected_html = '<div id="ebeveyn-id" class="ebeveyn-sinif"><span>Span child</span><em>Em child</em></div>'
        # Eğer sıra önemliyse ve 3.7+ kullanmıyorsanız, çıktı stringini parse edip
        # özelliklerin varlığını ve değerlerini kontrol eden daha karmaşık bir test yazılmalıdır.
        self.assertEqual(parent_node.to_html(), expected_html)

    def test_to_html_empty_tag_raises_error(self):
        """
        Test case: ParentNode with empty tag when to_html() is called.
        Yinelemeli (redundant) bir kontrol ama metodun robustness'ını test eder.
        """
        # Önce geçerli bir node oluştur, sonra tag'ini geçersiz yap
        node = ParentNode("div", [LeafNode("span", "child")])
        node.tag = "" # Tag'i boş dize yap

        # to_html() çağrıldığında ValueError yükseldiğini kontrol et
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "Invalid HTML: ParentNode requires a tag to render")

    def test_to_html_no_children_raises_error(self):
        """
        Test case: ParentNode with no children when to_html() is called.
        Yinelemeli (redundant) bir kontrol ama metodun robustness'ını test eder.
        """
        # Önce geçerli bir node oluştur, sonra children'ı None veya boş liste yap
        node_none = ParentNode("div", [LeafNode("span", "child")])
        node_none.children = None # Children'ı None yap

        with self.assertRaises(ValueError) as cm:
            node_none.to_html()
        self.assertEqual(str(cm.exception), "Invalid HTML: ParentNode requires children to render")

        node_empty = ParentNode("div", [LeafNode("span", "child")])
        node_empty.children = [] # Children'ı boş liste yap

        with self.assertRaises(ValueError) as cm:
            node_empty.to_html()
        self.assertEqual(str(cm.exception), "Invalid HTML: ParentNode requires children to render")

class TestTextNodeToHTMLNodeConversion(unittest.TestCase):

    # Kullanıcı tarafından sağlanan başlangıç testi
    def test_text(self):
        """
        TextType.TEXT dönüşümünü test eder.
        """
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        # Sonucun bir LeafNode olduğunu kontrol et
        self.assertIsInstance(html_node, LeafNode)
        # tag, value ve props attribute'larının doğru ayarlandığını kontrol et
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.props) # Varsayılan olarak props None olmalı

    def test_bold(self):
        """
        TextType.BOLD dönüşümünü test eder.
        """
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertIsNone(html_node.props)
        # İsteğe bağlı: to_html çıktısını da kontrol et
        self.assertEqual(html_node.to_html(), "<b>This is bold text</b>")


    def test_italic(self):
        """
        TextType.ITALIC dönüşümünü test eder.
        """
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertIsNone(html_node.props)
        self.assertEqual(html_node.to_html(), "<i>This is italic text</i>")

    def test_code(self):
        """
        TextType.CODE dönüşümünü test eder.
        """
        node = TextNode("This is code block", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code block")
        self.assertIsNone(html_node.props)
        self.assertEqual(html_node.to_html(), "<code>This is code block</code>")

    def test_link(self):
        """
        TextType.LINK dönüşümünü test eder.
        """
        node = TextNode("Visit Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Visit Google")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        # Linkin to_html çıktısını kontrol et
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">Visit Google</a>')

    def test_link_no_url_raises_error(self):
        """
        TextType.LINK dönüşümünde url eksikse ValueError yükseltildiğini test eder.
        """
        node = TextNode("Visit Google", TextType.LINK, None) # url None

        # ValueError'ın yükseltildiğini kontrol et
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        # Yükseltilen hatanın mesajını kontrol et
        self.assertEqual(str(cm.exception), "Link TextNode must have a url")


    """def test_image(self):
        
        #TextType.IMAGE dönüşümünü test eder.
        
        node = TextNode("A nice image", TextType.IMAGE, "/path/to/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "") # img tag'inin value'su genellikle boş olur
        self.assertEqual(html_node.props, {"src": "/path/to/image.jpg", "alt": "A nice image"})
        # Resmin to_html çıktısını kontrol et
        self.assertEqual(html_node.to_html(), '<img src="/path/to/image.jpg" alt="A nice image">')
    """

    def test_image_no_url_raises_error(self):
        """
        TextType.IMAGE dönüşümünde url eksikse ValueError yükseltildiğini test eder.
        """
        node = TextNode("A nice image", TextType.IMAGE, None) # url None

        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "Image TextNode must have both url and text for alt attribute")

    def test_image_no_text_raises_error(self):
        """
        TextType.IMAGE dönüşümünde text (alt) eksikse ValueError yükseltildiğini test eder.
        """
        node = TextNode(None, TextType.IMAGE, "/path/to/image.jpg") # text None

        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "Image TextNode must have both url and text for alt attribute")


    def test_unhandled_type_raises_error(self):
        """
        TextNode'un text_type'ı tanımlı değilse ValueError yükseltildiğini test eder.
        """
        # Test için geçici, bilinmeyen bir TextType üyesi oluşturalım
        class UnhandledTextType(Enum):
            UNKNOWN = "unknown"

        # Test için TextNode'un yapısını taklit eden basit bir sınıf oluşturalım
        # (Normalde gerçek TextNode constructor'ı TextType'ı kontrol eder, bu test
        # o kontrolü atlayan bir senaryoyu simüle eder veya başka bir modülden gelen
        # bilinmeyen bir tip olduğunu varsayar.)
        class MockTextNode:
            def __init__(self, text, text_type, url=None):
                self.text = text
                self.text_type = text_type
                self.url = url
            # Diğer metotlar (repr, eq) test için gerekli değil

        node = MockTextNode("This node has a weird type", UnhandledTextType.UNKNOWN)

        # ValueError'ın yükseltildiğini kontrol et
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        # Yükseltilen hatanın mesajını kontrol et
        self.assertEqual(str(cm.exception), f"Unhandled text node type: {UnhandledTextType.UNKNOWN}")



# This block allows you to run the tests directly from the script
if __name__ == "__main__":
    unittest.main()