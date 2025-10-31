
import xml.etree.ElementTree as ET


class Argument:
    '''Class representing an argument to a modular input kind.
    ``Argument`` is meant to be used with ``Scheme`` to generate an XML
    definition of the modular input kind that Splunk understands.
    ``name`` is the only required parameter for the constructor.
    '''

    data_type_string = "string"
    data_type_number = "number"
    data_type_boolean = "boolean"

    def __init__(self, name, description=None, validation=None, data_type=data_type_string, required_on_edit=False, required_on_create=False, title=None):
        self.name = name
        self.description = description
        self.validation = validation
        self.data_type = data_type
        self.required_on_edit = required_on_edit
        self.required_on_create = required_on_create
        self.title = title

    def add_to_document(self, parent):
        arg_element = ET.SubElement(parent, 'arg')
        ET.SubElement(arg_element, 'name').text = self.name
        if self.description:
            ET.SubElement(arg_element, 'description').text = self.description
        if self.validation:
            ET.SubElement(arg_element, 'validation').text = self.validation
        if self.data_type:
            ET.SubElement(arg_element, 'data_type').text = self.data_type
        if self.required_on_edit is not None:
            ET.SubElement(arg_element, 'required_on_edit').text = str(
                self.required_on_edit).lower()
        if self.required_on_create is not None:
            ET.SubElement(arg_element, 'required_on_create').text = str(
                self.required_on_create).lower()
        if self.title:
            ET.SubElement(arg_element, 'title').text = self.title
        return arg_element
