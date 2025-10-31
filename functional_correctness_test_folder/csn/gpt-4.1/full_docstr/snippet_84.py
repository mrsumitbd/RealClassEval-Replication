
import xml.etree.ElementTree as ET


class Scheme:
    '''Class representing the metadata for a modular input kind.
    A ``Scheme`` specifies a title, description, several options of how Splunk should run modular inputs of this
    kind, and a set of arguments which define a particular modular input's properties.
    The primary use of ``Scheme`` is to abstract away the construction of XML to feed to Splunk.
    '''

    def __init__(self, title):
        '''
        :param title: ``string`` identifier for this Scheme in Splunk.
        '''
        self.title = title
        self.description = None
        self.use_external_validation = False
        self.use_single_instance = False
        self.streaming_mode = None
        self.arguments = []

    def add_argument(self, arg):
        '''Add the provided argument, ``arg``, to the ``self.arguments`` list.
        :param arg: An ``Argument`` object to add to ``self.arguments``.
        '''
        self.arguments.append(arg)

    def to_xml(self):
        '''Creates an ``ET.Element`` representing self, then returns it.
        :returns: an ``ET.Element`` representing this scheme.
        '''
        scheme = ET.Element('scheme')

        title_elem = ET.SubElement(scheme, 'title')
        title_elem.text = self.title

        if self.description is not None:
            desc_elem = ET.SubElement(scheme, 'description')
            desc_elem.text = self.description

        ext_val_elem = ET.SubElement(scheme, 'use_external_validation')
        ext_val_elem.text = 'true' if self.use_external_validation else 'false'

        single_inst_elem = ET.SubElement(scheme, 'use_single_instance')
        single_inst_elem.text = 'true' if self.use_single_instance else 'false'

        if self.streaming_mode is not None:
            streaming_elem = ET.SubElement(scheme, 'streaming_mode')
            streaming_elem.text = self.streaming_mode

        if self.arguments:
            args_elem = ET.SubElement(scheme, 'endpoint')
            args_list_elem = ET.SubElement(args_elem, 'args')
            for arg in self.arguments:
                # Assume arg has a to_xml() method returning an ET.Element
                args_list_elem.append(arg.to_xml())

        return scheme
