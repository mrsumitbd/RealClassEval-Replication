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
        if not isinstance(title, str) or not title:
            raise ValueError("title must be a non-empty string")
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
        if arg is None:
            raise ValueError("arg cannot be None")
        if not hasattr(arg, "to_xml") or not callable(getattr(arg, "to_xml")):
            raise TypeError(
                "arg must have a to_xml() method returning an ET.Element")
        self.arguments.append(arg)

    def to_xml(self):
        '''Creates an ``ET.Element`` representing self, then returns it.
        :returns: an ``ET.Element`` representing this scheme.
        '''
        scheme_el = ET.Element("scheme")

        title_el = ET.SubElement(scheme_el, "title")
        title_el.text = self.title

        desc_el = ET.SubElement(scheme_el, "description")
        desc_el.text = self.description if self.description is not None else ""

        uev_el = ET.SubElement(scheme_el, "use_external_validation")
        uev_el.text = "true" if self.use_external_validation else "false"

        sm_el = ET.SubElement(scheme_el, "streaming_mode")
        sm_el.text = self.streaming_mode

        usi_el = ET.SubElement(scheme_el, "use_single_instance")
        usi_el.text = "true" if self.use_single_instance else "false"

        args_el = ET.SubElement(scheme_el, "arguments")
        for arg in self.arguments:
            arg_el = arg.to_xml()
            if not isinstance(arg_el, ET.Element):
                raise TypeError(
                    "Argument.to_xml() must return an xml.etree.ElementTree.Element")
            args_el.append(arg_el)

        return scheme_el
