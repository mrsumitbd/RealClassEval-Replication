import xml.etree.ElementTree as ET


class Scheme:
    '''Class representing the metadata for a modular input kind.
    A ``Scheme`` specifies a title, description, several options of how Splunk should run modular inputs of this
    kind, and a set of arguments which define a particular modular input's properties.
    The primary use of ``Scheme`` is to abstract away the construction of XML to feed to Splunk.
    '''

    def __init__(self, title):
        if not title:
            raise ValueError("title must be a non-empty string")
        self.title = title
        self.description = None
        self.use_external_validation = False
        self.streaming_mode = 'xml'
        self.use_single_instance = False
        self.arguments = []

    def add_argument(self, arg):
        '''Add the provided argument, ``arg``, to the ``self.arguments`` list.
        :param arg: An ``Argument`` object to add to ``self.arguments``.
        '''
        if arg is None:
            raise ValueError("arg cannot be None")
        self.arguments.append(arg)
        return self

    def to_xml(self):
        '''Creates an ``ET.Element`` representing self, then returns it.
        :returns: an ``ET.Element`` representing this scheme.
        '''
        scheme = ET.Element('scheme')

        title_el = ET.SubElement(scheme, 'title')
        title_el.text = str(self.title)

        if self.description is not None:
            desc_el = ET.SubElement(scheme, 'description')
            desc_el.text = str(self.description)

        ext_val_el = ET.SubElement(scheme, 'use_external_validation')
        ext_val_el.text = 'true' if self.use_external_validation else 'false'

        streaming_el = ET.SubElement(scheme, 'streaming_mode')
        streaming_el.text = str(self.streaming_mode)

        single_inst_el = ET.SubElement(scheme, 'use_single_instance')
        single_inst_el.text = 'true' if self.use_single_instance else 'false'

        endpoint_el = ET.SubElement(scheme, 'endpoint')
        args_el = ET.SubElement(endpoint_el, 'args')

        for arg in self.arguments:
            if hasattr(arg, 'to_xml') and callable(arg.to_xml):
                arg_el = arg.to_xml()
                args_el.append(arg_el)
            else:
                # Fallback minimal representation if no to_xml available
                ET.SubElement(args_el, 'arg', {'name': str(arg)})

        return scheme
