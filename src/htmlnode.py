

class HTMLNode():
    def __init__(self,tag = None,value = None,children = None,props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise(NotImplementedError)
    
    def props_to_html(self):
        if self.props is None or not self.props: # Check if props is None or empty dict
            return ""
        attribute_parts = []
        for key, value in self.props.items():
            # Format each key-value pair as key="value"
            # Ensure values are strings or convertible to strings
            attribute_parts.append(f'{key}="{value}"')
        
        return " " + " ".join(attribute_parts)
    
    def __repr__(self):
        return (f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
                f"children={self.children!r}, props={self.props!r})")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode requires a value")
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: LeafNode must have a value")
        
        if self.tag is None:
            return self.value
        
        attributes_html = self.props_to_html()
        return f"<{self.tag}{attributes_html}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children , props=None):
       
        if tag is None or tag == "":
            raise ValueError("ParentNode requires a tag")
        
        if children is None or not isinstance(children, list) or len(children) == 0:
            raise ValueError("ParentNode requires a non-empty list of children")
        
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("Invalid HTML: ParentNode requires a tag to render")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Invalid HTML: ParentNode requires children to render")
        children_html_string = ""
        for child in self.children:
            children_html_string += child.to_html()
        attributes_html = self.props_to_html()
        return f"<{self.tag}{attributes_html}>{children_html_string}</{self.tag}>"
        
