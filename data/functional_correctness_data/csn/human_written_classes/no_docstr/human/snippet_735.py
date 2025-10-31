import os
from lxml import etree

class XMLParser:

    def __init__(self, schema_dir, schema_file):
        orig_path = os.path.abspath(os.curdir)
        os.chdir(schema_dir)
        with open(schema_file, 'r') as f:
            schema = etree.XMLSchema(etree.XML(f.read().encode('utf-8')))
        os.chdir(orig_path)
        self._parser = etree.XMLParser(schema=schema, remove_comments=True, remove_blank_text=False)

    def parse(self, txt: str):
        if not isinstance(txt, str):
            raise ValueError('txt must be a str')
        xml_file = txt.encode('utf-8')
        return etree.fromstring(xml_file, self._parser)