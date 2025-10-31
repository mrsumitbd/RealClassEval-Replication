
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
        self.description = ''
        self.use_external_validation = False
        self.streaming_mode = False
        self.use_single_instance = False
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
        scheme_el = ET.Element('scheme')

        title_el = ET.SubElement(scheme_el, 'title')
        title_el.text = self.title

        desc_el = ET.SubElement(scheme_el, 'description')
        desc_el.text = self.description

        ext_val_el = ET.SubElement(scheme_el, 'use_external_validation')
        ext_val_el.text = str(self.use_external_validation).lower()

        stream_el = ET.SubElement(scheme_el, 'streaming_mode')
        stream_el.text = str(self.streaming_mode).lower()

        single_inst_el = ET.SubElement(scheme_el, 'use_single_instance')
        single_inst_el.text = str(self.use_single_instance).lower()

        for arg in self.arguments:
            scheme_el.append(arg.to_xml())

        return scheme_el
