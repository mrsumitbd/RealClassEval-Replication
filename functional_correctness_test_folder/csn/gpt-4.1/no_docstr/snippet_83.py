
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

    def __init__(self, name, description=None, validation=None, data_type=None, required_on_edit=False, required_on_create=False, title=None):
        if data_type is None:
            data_type = Argument.data_type_string
        self.name = name
        self.description = description
        self.validation = validation
        self.data_type = data_type
        self.required_on_edit = required_on_edit
        self.required_on_create = required_on_create
        self.title = title

    def add_to_document(self, parent):
        import xml.etree.ElementTree as ET

        arg_elem = ET.SubElement(parent, "arg")
        arg_elem.set("name", self.name)
        if self.data_type:
            arg_elem.set("type", self.data_type)
        if self.required_on_edit:
            arg_elem.set("required_on_edit", "true")
        if self.required_on_create:
            arg_elem.set("required_on_create", "true")
        if self.title is not None:
            title_elem = ET.SubElement(arg_elem, "title")
            title_elem.text = self.title
        if self.description is not None:
            desc_elem = ET.SubElement(arg_elem, "description")
            desc_elem.text = self.description
        if self.validation is not None:
            val_elem = ET.SubElement(arg_elem, "validation")
            val_elem.text = self.validation
        return arg_elem
