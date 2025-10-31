class popup:
    """An information box used when hovering over a node.

    It takes a list of alternating texts to display.
    """

    def __init__(self, _ctx, node, texts=None, width=200, speed=2.0):
        if texts != None and (not isinstance(texts, (tuple, list))):
            texts = [texts]
        self._ctx = _ctx
        self.node = node
        self.i = 0
        self.q = texts
        if self.q == None:
            self.q = []
            try:
                id = str(self.node.id)
                for i in range(wordnet.count_senses(id)):
                    txt = id + ' | ' + wordnet.gloss(id, sense=i)
                    self.q.append(txt)
            except:
                pass
        self.background = self._ctx.color(0.0, 0.1, 0.15, 0.6)
        self.text = self._ctx.color(1.0, 1.0, 1.0, 0.8)
        self.font = 'Verdana'
        self.fontsize = 9.5
        self._textpaths = []
        self._w = width
        self.speed = speed
        self.delay = 20 / self.speed
        self.fi = 0
        self.fn = 0
        self.mf = 50

    def textpath(self, i):
        """Returns a cached textpath of the given text in queue."""
        if len(self._textpaths) == i:
            self._ctx.font(self.font, self.fontsize)
            txt = self.q[i]
            if len(self.q) > 1:
                txt += ' (' + str(i + 1) + '/' + str(len(self.q)) + ')'
            p = self._ctx.textpath(txt, 0, 0, width=self._w)
            h = self._ctx.textheight(txt, width=self._w)
            self._textpaths.append((p, h))
        return self._textpaths[i]

    def update(self):
        """Rotates the queued texts and determines display time."""
        if self.delay > 0:
            self.delay -= 1
            return
        if self.fi == 0:
            if len(self.q) == 1:
                self.fn = float('inf')
            else:
                self.fn = len(self.q[self.i]) / self.speed
                self.fn = max(self.fn, self.mf)
        self.fi += 1
        if self.fi > self.fn:
            self.fi = 0
            self.i = (self.i + 1) % len(self.q)

    def draw(self):
        """Draws a popup rectangle with a rotating text queue."""
        if len(self.q) > 0:
            self.update()
            if self.delay == 0:
                p, h = self.textpath(self.i)
                f = self.fontsize
                self._ctx.fill(self.background)
                self._ctx.rect(self.node.x + f * 1.0, self.node.y + f * 0.5, self._w + f, h + f * 1.5, roundness=0.2)
                alpha = 1.0
                if self.fi < 5:
                    alpha = 0.2 * self.fi
                if self.fn - self.fi < 5:
                    alpha = 0.2 * (self.fn - self.fi)
                self._ctx.fill(self.text.r, self.text.g, self.text.b, self.text.a * alpha)
                self._ctx.translate(self.node.x + f * 2.0, self.node.y + f * 2.5)
                self._ctx.drawpath(p)