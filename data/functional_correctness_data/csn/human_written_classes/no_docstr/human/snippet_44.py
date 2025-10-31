class Graftmap:

    def __del__(self):
        if not type(self) is Graftmap:
            return
        self.thisown = False

    def __init__(self, doc):
        dst = _as_pdf_document(doc)
        map_ = mupdf.pdf_new_graft_map(dst)
        self.this = map_
        self.thisown = True