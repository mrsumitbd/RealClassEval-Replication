import xml.etree.ElementTree as ET


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

    data_type_string = 'string'
    data_type_number = 'number'
    data_type_boolean = 'boolean'

    def __init__(self, name, description=None, validation=None, data_type=data_type_string, required_on_edit=False, required_on_create=False, title=None):
        if not name or not isinstance(name, str):
            raise ValueError("Argument 'name' must be a non-empty string")
        self.name = name
        self.description = description
        self.validation = validation
        self.data_type = data_type or self.data_type_string
        self.required_on_edit = bool(required_on_edit)
        self.required_on_create = bool(required_on_create)
        self.title = title

    def add_to_document(self, parent):
        arg_elem = ET.SubElement(parent, 'arg', {'name': self.name})

        if self.title is not None:
            title_el = ET.SubElement(arg_elem, 'title')
            title_el.text = str(self.title)

        if self.description is not None:
            desc_el = ET.SubElement(arg_elem, 'description')
            desc_el.text = str(self.description)

        if self.data_type is not None:
            dt_el = ET.SubElement(arg_elem, 'data_type')
            dt_el.text = str(self.data_type)

        if self.validation is not None:
            val_el = ET.SubElement(arg_elem, 'validation')
            val_el.text = str(self.validation)

        roe_el = ET.SubElement(arg_elem, 'required_on_edit')
        roe_el.text = 'true' if self.required_on_edit else 'false'

        roc_el = ET.SubElement(arg_elem, 'required_on_create')
        roc_el.text = 'true' if self.required_on_create else 'false'

        return arg_elem
