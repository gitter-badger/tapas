#   just some experimental code for markdown processing
#   not yet usable and not used in the project

import markdown
from markdown.inlinepatterns import Pattern
from markdown.extensions import Extension
from markdown.util import etree

class InternalRef(Pattern):
    def __init__(self):
        Pattern.__init__(self, r"\$(.*?)\$")

    def handleMatch(self, m):
        el = etree.Element('b')
        el.text = "InternalRef:" + m.group(2)
        return el

internalRef = InternalRef()


class InternalRefExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('internalRef', InternalRef(), "_end")

proc = markdown.Markdown(extensions=[InternalRefExtension()])

print(proc.convert("some $blabla$ text"))
