class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        prop_items = self.props.items()
        string = ""
        for item in prop_items:
            string += ' ' + item[0] + '="' + item[1] + '"'
        return string

    def __repr__(self):
        return f"HTMLNode: {self.tag}, {self.value}, Children: {self.children}, {self.props}"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag!")
        if self.children is None:
            raise ValueError("no children!")
        return_string = f"<{self.tag}>"
        for child in self.children:
            return_string += child.to_html()
        return_string += f"</{self.tag}>"
        return return_string
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"    
