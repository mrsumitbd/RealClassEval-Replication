class ToC:

    def __init__(self) -> None:
        self.first_toc_entry = True
        self.numbering = [0]
        self.toc = ''
        self.start_numbering = True

    def add_entry(self, thisdepth: int, title: str) -> str:
        """Add an entry to the table of contents."""
        depth = len(self.numbering)
        if thisdepth < depth:
            self.toc += '</ol>'
            for _ in range(0, depth - thisdepth):
                self.numbering.pop()
                self.toc += '</li></ol>'
            self.numbering[-1] += 1
        elif thisdepth == depth:
            if not self.first_toc_entry:
                self.toc += '</ol>'
            else:
                self.first_toc_entry = False
            self.numbering[-1] += 1
        elif thisdepth > depth:
            self.numbering.append(1)
        num = '{}.{}'.format(self.numbering[0], '.'.join([str(n) for n in self.numbering[1:]])) if self.start_numbering else ''
        self.toc += f'<li><a href="#{to_id(title)}">{num} {title}</a><ol>\n'
        return num

    def contents(self, idn: str) -> str:
        toc = '<h1 id="{}">Table of contents</h1>\n               <nav class="tocnav"><ol>{}'.format(idn, self.toc)
        toc += '</ol>'
        for _ in range(0, len(self.numbering)):
            toc += '</li></ol>'
        toc += '</nav>'
        return toc