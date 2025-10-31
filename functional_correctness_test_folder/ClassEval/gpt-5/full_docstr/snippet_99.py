
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
from typing import List, Optional


class XMLProcessor:
    """
    This is a class as XML files handler, including reading, writing, processing as well as finding elements in a XML file.
    """

    def __init__(self, file_name):
        """
        Initialize the XMLProcessor object with the given file name.
        :param file_name:string, the name of the XML file to be processed.
        """
        self.file_name = file_name
        self.root: Optional[Element] = None
        self._tree: Optional[ET.ElementTree] = None

    def read_xml(self):
        """
        Reads the XML file and returns the root element.
        :return: Element, the root element of the XML file.
        >>> xml_processor = XMLProcessor('test.xml')
        >>> root_element = xml_processor.read_xml()
        >>> print(root_element)
        <Element 'root' at 0x7f8e3b7eb180>
        """
        try:
            self._tree = ET.parse(self.file_name)
            self.root = self._tree.getroot()
            return self.root
        except Exception:
            self._tree = None
            self.root = None
            return None

    def write_xml(self, file_name):
        """
        Writes the XML data to the specified file.
        :param file_name: string, the name of the file to write the XML data.
        :return: bool, True if the write operation is successful, False otherwise.
        >>> xml_processor = XMLProcessor('test.xml')
        >>> root = xml_processor.read_xml()
        >>> success = xml_processor.write_xml('output.xml')
        >>> print(success)
        True
        """
        if self.root is None:
            return False
        try:
            tree = self._tree if self._tree is not None else ET.ElementTree(
                self.root)
            tree.write(file_name, encoding='utf-8', xml_declaration=True)
            return True
        except Exception:
            return False

    def process_xml_data(self, file_name):
        """
        Modifies the data in XML elements and writes the updated XML data to a new file.
        :param file_name: string, the name of the file to write the modified XML data.
        :return: bool, True if the write operation is successful, False otherwise.
        >>> xml_processor = XMLProcessor('test.xml')
        >>> root = xml_processor.read_xml()
        >>> success = xml_processor.process_xml_data('processed.xml')
        >>> print(success)
        True
        """
        if self.root is None:
            return False
        try:
            for elem in self.root.iter():
                if elem.text is not None:
                    elem.text = elem.text.strip()
                # mark as processed
                elem.set('processed', 'true')
            tree = self._tree if self._tree is not None else ET.ElementTree(
                self.root)
            tree.write(file_name, encoding='utf-8', xml_declaration=True)
            return True
        except Exception:
            return False

    def find_element(self, element_name):
        """
        Finds the XML elements with the specified name.
        :param element_name: string, the name of the elements to find.
        :return: list, a list of found elements with the specified name.
        >>> xml_processor = XMLProcessor('test.xml')
        >>> root = xml_processor.read_xml()
        >>> items = xml_processor.find_element('item')
        >>> for item in items:
        >>>     print(item.text)
        apple
        banana
        orange
        """
        if not element_name or self.root is None:
            return []
        try:
            return list(self.root.iter(element_name))
        except Exception:
            return []
