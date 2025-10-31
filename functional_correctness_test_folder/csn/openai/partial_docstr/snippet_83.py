
import xml.etree.ElementTree as ET


class Argument:
    """Class representing an argument to a modular input kind.

    ``Argument`` is meant to be used with ``Scheme`` to generate an XML
    definition of the modular input kind that Splunk understands.
    ``name`` is the only required parameter for the constructor.

    Example with least parameters::
        arg1 = Argument(name="arg1")

    Example with all parameters::
        arg2 = Argument(
            name="arg2",
            description="This is an argument with lots of parameters",
            validation="is_pos_int('some_name')",
            data_type=Argument.data_type_number,
            required_on_edit=True,
            required_on_create=True
        )
    """

    # Data type constants
    data_type_string = "string"
    data_type_number = "number"
    data_type_boolean = "boolean"

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
        :param validation: ``string`` specifying how the argument should be validated,
                           if using internal validation. If using external validation,
                           this will be ignored.
        :param data_type: ``string``, data type of this field; use the class constants.
                          "data_type_boolean", "data_type_number", or "data_type_string".
        :param required_on_edit: ``Boolean``, whether this arg is required when editing an
                                 existing modular input of this kind.
        :param required_on_create: ``Boolean``, whether this arg is required when creating a
                                   modular input of this kind.
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
        """Adds an ``Argument`` object to this ElementTree document.

        Adds an <arg> subelement to the parent element, typically <args>
        and sets up its subelements with their respective text.

        :param parent: An ``ET.Element`` to be the parent of a new <arg> subelement
        :returns: An ``ET.Element`` object representing this argument.
        """
        arg_el = ET.SubElement(parent, "arg")

        # Helper to add subelement if value is not None
        def _add_sub(name, value):
            if value is not None:
                sub = ET.SubElement(arg_el, name)
                sub.text = str(value)

        _add_sub("name", self.name)
        _add_sub("title", self.title)
        _add_sub("description", self.description)
        _add_sub("data_type", self.data_type)
        _add_sub("validation", self.validation)
        _add_sub("required_on_edit",
                 "true" if self.required_on_edit else "false")
        _add_sub("required_on_create",
                 "true" if self.required_on_create else "false")

        return arg_el
