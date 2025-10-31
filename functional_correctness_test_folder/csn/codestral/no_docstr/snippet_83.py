
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
        arg = parent.addElement("arg")
        arg.setAttribute("name", self.name)
        if self.description is not None:
            arg.setAttribute("description", self.description)
        if self.validation is not None:
            arg.setAttribute("validation", self.validation)
        if self.data_type is not None:
            arg.setAttribute("data_type", self.data_type)
        if self.required_on_edit:
            arg.setAttribute("required_on_edit", "true")
        else:
            arg.setAttribute("required_on_edit", "false")
        if self.required_on_create:
            arg.setAttribute("required_on_create", "true")
        else:
            arg.setAttribute("required_on_create", "false")
        if self.title is not None:
            arg.setAttribute("title", self.title)
