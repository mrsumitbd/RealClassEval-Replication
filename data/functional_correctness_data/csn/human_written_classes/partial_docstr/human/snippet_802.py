from xml.sax import make_parser, ContentHandler, parseString
from xml.sax.handler import feature_external_ges
from suds import metrics

class Parser:
    """ SAX Parser """

    @classmethod
    def saxparser(cls):
        p = make_parser()
        p.setFeature(feature_external_ges, 0)
        h = Handler()
        p.setContentHandler(h)
        return (p, h)

    def parse(self, file=None, string=None):
        """
        SAX parse XML text.
        @param file: Parse a python I{file-like} object.
        @type file: I{file-like} object.
        @param string: Parse string XML.
        @type string: str
        """
        timer = metrics.Timer()
        timer.start()
        sax, handler = self.saxparser()
        if file is not None:
            sax.parse(file)
            timer.stop()
            metrics.log.debug('sax (%s) duration: %s', file, timer)
            return handler.nodes[0]
        if string is not None:
            if isinstance(string, str):
                string = string.encode()
            parseString(string, handler)
            timer.stop()
            metrics.log.debug('%s\nsax duration: %s', string, timer)
            return handler.nodes[0]