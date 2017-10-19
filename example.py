# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import codecs
import cProfile
import logging
import re
from pstats import Stats

from bs4 import BeautifulSoup

# draftjs_exporter provides default configurations and predefined constants for reuse.
from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES, INLINE_STYLES
from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP
from draftjs_exporter.dom import DOM
from draftjs_exporter.html import HTML


def Image(props):
    """
    <embed alt="Right-aligned image" embedtype="image" format="right" id="1"/>
    """
    return DOM.create_element('embed', {
        'embedtype': 'image',
        'format': props.get('alignment'),
        'id': props.get('id'),
        'alt': props.get('altText'),
    })


def Embed(props):
    """
    <embed embedtype="media" url="https://www.youtube.com/watch?v=y8Kyi0WNg40"/>
    """
    return DOM.create_element('embed', {
        'embedtype': 'media',
        'url': props.get('url'),
    })


def Document(props):
    """
    <a id="1" linktype="document">document link</a>
    """

    return DOM.create_element('a', {
        'linktype': 'document',
        'id': props.get('id'),
    }, props['children'])


def Link(props):
    """
    <a linktype="page" id="1">internal page link</a>
    """
    link_type = props.get('linkType', '')
    link_props = {}

    if link_type == 'page':
        link_props['linktype'] = link_type
        link_props['id'] = props.get('id')
    else:
        link_props['href'] = props.get('url')

    return DOM.create_element('a', link_props, props['children'])


class BR:
    """
    Replace line breaks (\n) with br tags.
    """
    SEARCH_RE = re.compile(r'\n')

    def render(self, props):
        # Do not process matches inside code blocks.
        if props['block']['type'] == BLOCK_TYPES.CODE:
            return props['children']

        return DOM.create_element('br')


def BlockFallback(props):
    type_ = props['block']['type']
    logging.error('Missing config for "%s". Deleting block.' % type_)
    return None


def EntityFallback(props):
    type_ = props['entity']['type']
    logging.warn('Missing config for "%s". Deleting entity' % type_)
    return None


config = {
    # Use the default draftjs_exporter block map.
    'block_map': dict(BLOCK_MAP, **{
        BLOCK_TYPES.FALLBACK: BlockFallback,
    }),
    # Use the default draftjs_exporter style map.
    'style_map': dict(STYLE_MAP, **{
        INLINE_STYLES.BOLD: 'b',
        INLINE_STYLES.ITALIC: 'i',
    }),
    'entity_decorators': {
        ENTITY_TYPES.IMAGE: Image,
        ENTITY_TYPES.LINK: Link,
        ENTITY_TYPES.DOCUMENT: Document,
        ENTITY_TYPES.HORIZONTAL_RULE: lambda props: DOM.create_element('hr'),
        ENTITY_TYPES.EMBED: Embed,
        ENTITY_TYPES.FALLBACK: EntityFallback,
    },
    'composite_decorators': [
        BR,
    ],
    'engine': 'html5lib',
}

exporter = HTML(config)

# DB-HTML of Wagtail with Hallo: <p>Paragraph text <a id="1" linktype="page">internal link text</a>, <a href="http://example.com">external link text</a>, <a href="mailto:test@example.com">email link text</a></p><p>Paragraph text <b>bold</b>,\u00a0<i>italic</i>, <b><i>bold italic</i></b>, <i><b>italic bold</b></i></p><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><p><ol><li>Ordered list item 1<br/></li><li>Ordered list item 2</li><li>Ordered list item 3</li></ol><p><ul><li>Unordered list item 1</li><li>Unordered list item 2</li><li>Unordered list item 3</li></ul><p>Horizontal rule:</p></p></p><p><hr/><embed embedtype="media" url="https://www.youtube.com/watch?v=y8Kyi0WNg40"/><p>Unstyled text after embed</p><p><br/></p><p>Paragraph <a id="1" linktype="document">document link</a></p><p><embed alt="Full width image" embedtype="image" format="fullwidth" id="1"/><br/></p></p><p><embed alt="Left-aligned image" embedtype="image" format="left" id="1"/></p><p>Text after left-aligned image</p><p><br/></p><p><br/></p><p><br/></p><p><embed alt="Right-aligned image" embedtype="image" format="right" id="1"/>Text after a right-aligned image</p><p><br/></p><p><br/></p><p><br/></p>
content_state = {
    "entityMap":{"0":{"type":"LINK","mutability":"MUTABLE","data":{"editUrl":"/admin/pages/3/edit/","parentId":1,"url":"/","id":1,"linkType":"page"}},"1":{"type":"LINK","mutability":"MUTABLE","data":{"url":"http://example.com","prefer_this_title_as_link_text":False,"linkType":"external"}},"2":{"type":"LINK","mutability":"MUTABLE","data":{"url":"mailto:test@example.com","prefer_this_title_as_link_text":False,"linkType":"email"}},"3":{"type":"HORIZONTAL_RULE","mutability":"IMMUTABLE","data":{}},"4":{"type":"EMBED","mutability":"IMMUTABLE","data":{"embedType":"media","url":"https://www.youtube.com/watch?v=y8Kyi0WNg40","providerName":"YouTube","authorName":"magnets99","thumbnail":"https://i.ytimg.com/vi/y8Kyi0WNg40/hqdefault.jpg","title":"Dramatic Look"}},"5":{"type":"DOCUMENT","mutability":"MUTABLE","data":{"id":1,"title":"Test document","url":"/documents/1/unsplash.md","edit_link":"/admin/documents/edit/1/"}},"6":{"type":"IMAGE","mutability":"IMMUTABLE","data":{"id":1,"edit_link":"/admin/images/1/","title":"Test image","preview":{"url":"/media/images/nasa.max-165x165.jpg","width":165,"height":109},"src":"/media/images/nasa.max-165x165.jpg","alignment":"fullwidth","altText":"Full-width image"}},"7":{"type":"IMAGE","mutability":"IMMUTABLE","data":{"id":1,"edit_link":"/admin/images/1/","title":"Test image","preview":{"url":"/media/images/nasa.max-165x165.jpg","width":165,"height":109},"src":"/media/images/nasa.max-165x165.jpg","alignment":"left","altText":"Left-aligned image"}},"8":{"type":"IMAGE","mutability":"IMMUTABLE","data":{"id":1,"edit_link":"/admin/images/1/","title":"Test image","preview":{"url":"/media/images/nasa.max-165x165.jpg","width":165,"height":109},"src":"/media/images/nasa.max-165x165.jpg","alignment":"right","altText":"Right-aligned image"}}},
    "blocks":[{"key":"3b9ec","text":"Paragraph text internal link text, external link text, email link text","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":15,"length":18,"key":0},{"offset":35,"length":18,"key":1},{"offset":55,"length":15,"key":2}],"data":{}},{"key":"agia4","text":"Paragraph text bold, italic, bold italic, italic bold","type":"unstyled","depth":0,"inlineStyleRanges":[{"offset":15,"length":4,"style":"BOLD"},{"offset":29,"length":11,"style":"BOLD"},{"offset":42,"length":11,"style":"BOLD"},{"offset":21,"length":6,"style":"ITALIC"},{"offset":29,"length":11,"style":"ITALIC"},{"offset":42,"length":11,"style":"ITALIC"}],"entityRanges":[],"data":{}},{"key":"3daa4","text":"Heading 2","type":"header-two","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"3dgg4","text":"Heading 3","type":"header-three","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"ee4jr","text":"Heading 4","type":"header-four","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"68dlm","text":"Ordered list item 1","type":"ordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"8jkbd","text":"Ordered list item 2","type":"ordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"be3ks","text":"Ordered list item 3","type":"ordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"a97qk","text":"Unordered list item 1","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"anslv","text":"Unordered list item 2","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"1utrr","text":"Unordered list item 3","type":"unordered-list-item","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"3lpbj","text":"Horizontal rule:","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"3e3lm","text":" ","type":"atomic","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":1,"key":3}],"data":{}},{"key":"unf5","text":" ","type":"atomic","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":1,"key":4}],"data":{}},{"key":"cgcis","text":"Unstyled text after embed","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"cg5t4","text":"Paragraph document link","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":10,"length":13,"key":5}],"data":{}},{"key":"eda0k","text":" ","type":"atomic","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":1,"key":6}],"data":{}},{"key":"dsnjc","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"bjefr","text":" ","type":"atomic","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":1,"key":7}],"data":{}},{"key":"22aql","text":"Text after left-aligned image, rendering underneath in Draft.js","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}},{"key":"1gh0q","text":" ","type":"atomic","depth":0,"inlineStyleRanges":[],"entityRanges":[{"offset":0,"length":1,"key":8}],"data":{}},{"key":"4tkgs","text":"Text after right-aligned image, rendering underneath in Draft.js","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}]
}

pr = cProfile.Profile()
pr.enable()

markup = exporter.render(content_state)

pr.disable()
p = Stats(pr)


def prettify(markup):
    return re.sub(r'</?(body|html|head)>', '', BeautifulSoup(markup, 'html5lib').prettify()).strip()


pretty = prettify(markup)

# Display in console.
print(pretty)

p.strip_dirs().sort_stats('cumulative').print_stats(0)

styles = """
/* Tacit CSS framework https://yegor256.github.io/tacit/ */
input,textarea,select,button,html,body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;font-stretch:normal;font-style:normal;font-weight:300;line-height:29.7px}input,textarea,select,button,html,body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;font-stretch:normal;font-style:normal;font-weight:300;line-height:29.7px}th{font-weight:600}td,th{border-bottom:1.08px solid #ccc;padding:14.85px 18px}thead th{border-bottom-width:2.16px;padding-bottom:6.3px}table{display:block;max-width:100%;overflow-x:auto}input,textarea,select,button,html,body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;font-stretch:normal;font-style:normal;font-weight:300;line-height:29.7px}input,textarea,select,button{display:block;max-width:100%;padding:9.9px}label{display:block;margin-bottom:14.76px}input[type="submit"],input[type="reset"],button{background:#f2f2f2;border-radius:3.6px;color:#8c8c8c;cursor:pointer;display:inline;margin-bottom:18px;margin-right:7.2px;padding:6.525px 23.4px;text-align:center}input[type="submit"]:hover,input[type="reset"]:hover,button:hover{background:#d9d9d9;color:#000}input[type="submit"][disabled],input[type="reset"][disabled],button[disabled]{background:#e6e6e6;color:#b3b3b3;cursor:not-allowed}input[type="submit"],button[type="submit"]{background:#367ac3;color:#fff}input[type="submit"]:hover,button[type="submit"]:hover{background:#255587;color:#bfbfbf}input[type="text"],input[type="password"],input[type="email"],input[type="url"],input[type="phone"],input[type="tel"],input[type="number"],input[type="datetime"],input[type="date"],input[type="month"],input[type="week"],input[type="color"],input[type="time"],input[type="search"],input[type="range"],input[type="file"],input[type="datetime-local"],select,textarea{border:1px solid #ccc;margin-bottom:18px;padding:5.4px 6.3px}input[type="checkbox"],input[type="radio"]{float:left;line-height:36px;margin-right:9px;margin-top:8.1px}input,textarea,select,button,html,body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;font-stretch:normal;font-style:normal;font-weight:300;line-height:29.7px}pre,code,kbd,samp,var,output{font-family:Menlo,Monaco,Consolas,"Courier New",monospace;font-size:16.2px}pre{border-left:1.8px solid #96bbe2;line-height:25.2px;margin-top:29.7px;overflow:auto;padding-left:18px}pre code{background:none;border:0;line-height:29.7px;padding:0}code{background:#ededed;border:1.8px solid #ccc;border-radius:3.6px;display:inline-block;line-height:18px;padding:3px 6px 2px}input,textarea,select,button,html,body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;font-stretch:normal;font-style:normal;font-weight:300;line-height:29.7px}h1,h2,h3,h4,h5,h6{color:#000;margin-bottom:18px}h1{font-size:36px;font-weight:500;margin-top:36px}h2{font-size:25.2px;font-weight:400;margin-top:27px}h3{font-size:21.6px;margin-top:21.6px}h4{font-size:18px;margin-top:18px}h5{font-size:14.4px;font-weight:bold;margin-top:18px;text-transform:uppercase}h6{color:#ccc;font-size:14.4px;font-weight:bold;margin-top:18px;text-transform:uppercase}input,textarea,select,button,html,body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;font-stretch:normal;font-style:normal;font-weight:300;line-height:29.7px}a{color:#367ac3;text-decoration:none}a:hover{text-decoration:underline}hr{border-bottom:1px solid #ccc}small{font-size:15.3px}em,i{font-style:italic}strong,b{font-weight:600}*{border:0;border-collapse:separate;border-spacing:0;box-sizing:border-box;margin:0;outline:0;padding:0;text-align:left;vertical-align:baseline}html,body{height:100%;width:100%}body{background:#f5f5f5;color:#1a1a1a;padding:36px}p,ul,ol,dl,blockquote,hr,pre,table,form,fieldset,figure,address{margin-bottom:29.7px}section{margin-left:auto;margin-right:auto;max-width:100%;width:900px}article{background:#fff;border:1.8px solid #d9d9d9;border-radius:7.2px;padding:43.2px}header{margin-bottom:36px}footer{margin-top:36px}nav{text-align:center}nav ul{list-style:none;margin-left:0;text-align:center}nav ul li{display:inline;margin-left:9px;margin-right:9px}nav ul li:first-child{margin-left:0}nav ul li:last-child{margin-right:0}ol,ul{margin-left:29.7px}li ol,li ul{margin-bottom:0}@media (max-width: 767px){body{padding:18px}article{border-radius:0;margin:-18px;padding:18px}textarea,input,select{max-width:100%}fieldset{min-width:0}section{width:auto}fieldset,x:-moz-any-link{display:table-cell}}
/* Custom styles to help with debugging */
blockquote { border-left: 0.25rem solid #aaa; padding-left: 1rem; font-style: italic; }
.u-text-center { text-align: center; }
a:hover, a:focus { outline: 1px solid red; }
.hashtag { color: pink; }
.list-item--depth-1 { margin-left: 5rem; }
"""

# Output to a styled HTML file for development.
with codecs.open('example.html', 'w', 'utf-8') as file:
    file.write("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>draftjs_exporter test page</title>
<style>{styles}</style>
</head>
<body>
    {html}
</body>
</html>
""".format(styles=styles, html=markup))

# Output to a Markdown file to showcase the output in GitHub (and see changes in git).
with codecs.open('docs/example.md', 'w', 'utf-8') as file:
    file.write("""
# Example output (generated by [`example.py`](../example.py))

-----
{html}
-----
""".format(html=pretty))
