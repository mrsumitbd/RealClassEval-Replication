import six
from abc import ABCMeta

@six.add_metaclass(ABCMeta)
class Parser:
    """Abstract parser class:

    Attributes:
      segmenter(:obj:`budou.segmenter.Segmenter`): Segmenter module.
    """

    def __init__(self):
        self.segmenter = None

    def parse(self, source, language=None, classname=None, max_length=None, attributes=None, inlinestyle=False, wbr=False):
        """Parses the source sentence to output organized HTML code.

        Args:
          source (str): Source sentence to process.
          language (str, optional): Language code.
          max_length (int, optional): Maximum length of a chunk.
          attributes (dict, optional): Attributes for output SPAN tags.
          inlinestyle (bool, optional): Add :code:`display:inline-block` as inline
                                        style attribute.
          wbr (bool, optional): User WBR tag for serialization.

        Returns:
          A dictionary containing :code:`chunks` (:obj:`budou.chunk.ChunkList`)
          and :code:`html_code` (str).
        """
        attributes = parse_attributes(attributes, classname, inlinestyle)
        source = preprocess(source)
        chunks = self.segmenter.segment(source, language)
        html_code = chunks.html_serialize(attributes, max_length=max_length, use_wbr=wbr)
        return {'chunks': chunks, 'html_code': html_code}