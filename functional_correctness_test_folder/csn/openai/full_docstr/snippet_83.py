
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

    # Data type constants
    data_type_string = "data_type_string"
    data_type_number = "data_type_number"
    data_type_boolean = "data_type_boolean"

    def __init__(
        self,
        name,
        description=None,
        validation=None,
        data_type=data_type_string,
        required_on_edit=False,
        required_on_create=False,
        title=None,
    ):
        """
        :param name: ``string``, identifier for this argument in Splunk.
        :param description: ``string``, human-readable description of the argument.
        :param validation: ``string`` specifying how the argument should be validated, if using internal validation.
               If using external validation, this will be ignored.
        :param data_type: ``string``, data type of this field; use the class constants.
               "data_type_boolean", "data_type_number", or "data_type_string".
        :param required_on_edit: ``Boolean``, whether this arg is required when editing an existing modular input of this kind.
        :param required_on_create: ``Boolean``, whether this arg is required when creating a modular input of this kind.
        :param title: ``String``, a human-readable title for the argument.
        """
        self.name = name
        self.description = description
        self.validation = validation
        self.data_type = data_type
        self.required_on_edit = required_on_edit
        self.required_on_create = required_on_create
        self.title = title

    def add_to_document(self, parent):
        """
        Adds an ``Argument`` object to this ElementTree document.
        Adds an <arg> subelement to the parent element, typically <args>
        and sets up its subelements with their respective text.
        :param parent: An ``ET.Element`` to be the parent of a new <arg> subelement
        :returns: An ``ET.Element`` object representing this argument.
        """
        arg_el = ET.SubElement(parent, "arg")

        # name (required)
        name_el = ET.SubElement(arg_el, "name")
        name_el.text = self.name

        # title (optional)
        if self.title is not None:
            title_el = ET.SubElement(arg_el, "title")
            title_el.text = self.title

        # description (optional)
        if self.description is not None:
            desc_el = ET.SubElement(arg_el, "description")
            desc_el.text = self.description

        # data_type (required)
        dt_el = ET.SubElement(arg_el, "data_type")
        dt_el.text = self.data_type

        # validation (optional)
        if self.validation is not None:
            val_el = ET.SubElement(arg_el, "validation")
            val_el.text = self.validation

        # required_on_edit (optional)
        if self.required_on_edit is not None:
            roe_el = ET.SubElement(arg_el, "required_on_edit")
            roe_el.text = "true" if self.required_on_edit else "false"

        # required_on_create (optional)
        if self.required_on_create is not None:
            roc_el = ET.SubElement(arg_el, "required_on_create")
            roc_el.text = "true" if self.required_on_create else "false"

        return arg_el
