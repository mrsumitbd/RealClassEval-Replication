
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
    data_type_integer = "integer"

    def __init__(self, name, description=None, validation=None, data_type=data_type_string, required_on_edit=False, required_on_create=False, title=None):
        self.name = name
        self.description = description
        self.validation = validation
        self.data_type = data_type
        self.required_on_edit = required_on_edit
        self.required_on_create = required_on_create
        self.title = title

    def add_to_document(self, parent):
        from xml.etree.ElementTree import SubElement

        arg_element = SubElement(parent, "arg")
        SubElement(arg_element, "name").text = self.name

        if self.title:
            SubElement(arg_element, "title").text = self.title

        if self.description:
            SubElement(arg_element, "description").text = self.description

        if self.data_type:
            SubElement(arg_element, "data_type").text = self.data_type

        if self.validation:
            SubElement(arg_element, "validation").text = self.validation

        if self.required_on_edit:
            SubElement(arg_element, "required_on_edit").text = "true"
        else:
            SubElement(arg_element, "required_on_edit").text = "false"

        if self.required_on_create:
            SubElement(arg_element, "required_on_create").text = "true"
        else:
            SubElement(arg_element, "required_on_create").text = "false"
