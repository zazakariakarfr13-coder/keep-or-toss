"""Tiny HTML tree helpers for tests and the site check."""
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children, self.text = [], []

    @property
    def classes(self):
        return (self.attrs.get("class") or "").split()

    def all_text(self):
        return "".join(self.text) + "".join(c.all_text() for c in self.children)

    def iter(self):
        yield self
        for c in self.children:
            yield from c.iter()

    def find_all(self, tag):
        return [n for n in self.iter() if n.tag == tag]


class _Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", [])
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.text.append(data)


def parse(html: str) -> Node:
    b = _Builder()
    b.feed(html)
    return b.root


def first_after_h1(root: Node):
    """The first element child of <main> after its <h1>, or None."""
    mains = root.find_all("main")
    if not mains:
        return None
    kids = mains[0].children
    for i, k in enumerate(kids):
        if k.tag == "h1":
            return kids[i + 1] if i + 1 < len(kids) else None
    return None
