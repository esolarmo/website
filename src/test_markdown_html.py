import unittest

from htmlnode import LeafNode
from markdown_html import *

class TestMarkdownToHTMLNode(unittest.TestCase):
        
    def test_paragraphs(self):
        self.maxDiff = None
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_quote(self):
        md = """
# Quotes

> This is a quote
> With some **bolded** sections
> and _italicized_ text

And also a normal paragraph.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            "<div><h1>Quotes</h1><blockquote>This is a quote\nWith some <b>bolded</b> sections\nand <i>italicized</i> text</blockquote><p>And also a normal paragraph.</p></div>",
        )

    def test_ulist(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ulist_complex(self):
        md = """
- **Item 1**
- _Item 2_
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            "<div><ul><li><b>Item 1</b></li><li><i>Item 2</i></li><li>Item 3</li></ul></div>",
        )

    def test_olist_complex(self):
        md = """
1. **Item 1**
2. _Item 2_
3. Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            "<div><ol><li><b>Item 1</b></li><li><i>Item 2</i></li><li>Item 3</li></ol></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_long_section(self):
        self.maxDiff = None
        md = """
### Heading 3

A story begins
with some background

#### Stuff to collect

- Mushrooms
- Berries
- Twigs

And get enough of everything.

#### Missions

1. Collect stuff
2. Kill the Dragon
3. Rejoice!

And do not forget to write some code

```
print("Hello World!")
```

Here is a [link](https://www.google.com) to google.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(
            html,
            '<div><h3>Heading 3</h3><p>A story begins with some background</p><h4>Stuff to collect</h4><ul><li>Mushrooms</li><li>Berries</li><li>Twigs</li></ul><p>And get enough of everything.</p><h4>Missions</h4><ol><li>Collect stuff</li><li>Kill the Dragon</li><li>Rejoice!</li></ol><p>And do not forget to write some code</p><pre><code>print("Hello World!")\n</code></pre><p>Here is a <a href="https://www.google.com">link</a> to google.</p></div>',
        )


class TestExtractTitle(unittest.TestCase):

    def test_title_found(self):
        md = """


# Title

Some paragraphs
"""
        title = extract_title(md)
        self.assertEqual(title, "Title")


    def test_title_not_found(self):
        md = """


- Title

Some paragraphs
"""
        self.assertRaises(Exception, extract_title, md)