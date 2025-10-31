
class Argument:
    '''Class representing an argument to a modular input kind.
    ``Argument`` is meant to be used with ``Scheme`` to generate an XML
    definition of the modular input kind that Splunk understands.
    ``name`` is the only required parameter for the constructor.
        **Example with least parameters**::
            arg1 = Argument(name="arg1")
        **Example with all parameters**::
            arg2 = Argument(
                name="arg2",
                description="This is an argument with lots of parameters",
                validation="is_pos_int('some_name')",
                data_type=Argument.data_type_number,
                required_on_edit=True,
                required_on_create=True
            )
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
        import xml.etree.ElementTree as ET
        arg_element = ET.SubElement(parent, "arg", name=self.name)

        if self.title:
            title_element = ET.SubElement(arg_element, "title")
            title_element.text = self.title

        if self.description:
            desc_element = ET.SubElement(arg_element, "description")
            desc_element.text = self.description

        if self.validation:
            validation_element = ET.SubElement(arg_element, "validation")
            validation_element.text = self.validation

        data_type_element = ET.SubElement(arg_element, "data_type")
        data_type_element.text = self.data_type

        required_on_edit_element = ET.SubElement(
            arg_element, "required_on_edit")
        required_on_edit_element.text = str(self.required_on_edit).lower()

        required_on_create_element = ET.SubElement(
            arg_element, "required_on_create")
        required_on_create_element.text = str(self.required_on_create).lower()
