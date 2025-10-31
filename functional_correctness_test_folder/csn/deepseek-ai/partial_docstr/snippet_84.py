
import xml.etree.ElementTree as ET


class Scheme:
    '''Class representing the metadata for a modular input kind.
    A ``Scheme`` specifies a title, description, several options of how Splunk should run modular inputs of this
    kind, and a set of arguments which define a particular modular input's properties.
    The primary use of ``Scheme`` is to abstract away the construction of XML to feed to Splunk.
    '''

    def __init__(self, title):
        self.title = title
        self.description = ""
        self.use_external_validation = False
        self.streaming_mode = "xml"
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
        scheme = ET.Element("scheme")

        title = ET.SubElement(scheme, "title")
        title.text = self.title

        description = ET.SubElement(scheme, "description")
        description.text = self.description

        external_validation = ET.SubElement(scheme, "use_external_validation")
        external_validation.text = str(self.use_external_validation).lower()

        streaming_mode = ET.SubElement(scheme, "streaming_mode")
        streaming_mode.text = self.streaming_mode

        use_single_instance = ET.SubElement(scheme, "use_single_instance")
        use_single_instance.text = str(self.use_single_instance).lower()

        if self.arguments:
            args_elem = ET.SubElement(scheme, "args")
            for arg in self.arguments:
                args_elem.append(arg.to_xml())

        return scheme
