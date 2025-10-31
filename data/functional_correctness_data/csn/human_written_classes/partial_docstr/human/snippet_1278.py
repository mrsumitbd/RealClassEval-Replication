from elifearticle import utils

class ContentBlock:

    def __init__(self, block_type=None, content=None, attr=None):
        self.block_type = block_type
        self.content = content
        self.content_blocks = []
        self.attr = {}
        if attr:
            self.attr = attr

    def attr_names(self):
        """list of tag attribute names"""
        return utils.attr_names(self.attr)

    def attr_string(self):
        """tag attributes formatted as a string"""
        return utils.attr_string(self.attr)