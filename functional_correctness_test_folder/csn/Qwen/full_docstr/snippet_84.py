
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
        self.description = ""
        self.use_external_validation = True
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
        root = ET.Element("scheme")
        title_elem = ET.SubElement(root, "title")
        title_elem.text = self.title

        if self.description:
            desc_elem = ET.SubElement(root, "description")
            desc_elem.text = self.description

        external_validation_elem = ET.SubElement(
            root, "use_external_validation")
        external_validation_elem.text = str(
            self.use_external_validation).lower()

        streaming_mode_elem = ET.SubElement(root, "streaming_mode")
        streaming_mode_elem.text = self.streaming_mode

        single_instance_elem = ET.SubElement(root, "use_single_instance")
        single_instance_elem.text = str(self.use_single_instance).lower()

        args_elem = ET.SubElement(root, "endpoint")
        args_elem.set("name", "arguments")

        for arg in self.arguments:
            arg_elem = ET.SubElement(args_elem, "arg")
            arg_elem.set("name", arg.name)
            if arg.description:
                desc_elem = ET.SubElement(arg_elem, "description")
                desc_elem.text = arg.description
            if arg.data_type:
                data_type_elem = ET.SubElement(arg_elem, "data_type")
                data_type_elem.text = arg.data_type
            if arg.required_on_create:
                required_on_create_elem = ET.SubElement(
                    arg_elem, "required_on_create")
                required_on_create_elem.text = str(
                    arg.required_on_create).lower()
            if arg.required_on_edit:
                required_on_edit_elem = ET.SubElement(
                    arg_elem, "required_on_edit")
                required_on_edit_elem.text = str(arg.required_on_edit).lower()

        return root


class Argument:
    def __init__(self, name, description="", data_type="string", required_on_create=False, required_on_edit=False):
        self.name = name
        self.description = description
        self.data_type = data_type
        self.required_on_create = required_on_create
        self.required_on_edit = required_on_edit
