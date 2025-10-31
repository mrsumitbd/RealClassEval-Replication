class NewickParser:
    """
    Class wrapping a parser for building Trees from newick format strings
    """

    def __init__(self):
        self.parser = create_parser()

    def parse_string(self, s):
        return self.parser.parseString(s)[0]