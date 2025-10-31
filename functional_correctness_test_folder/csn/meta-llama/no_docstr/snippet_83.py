
from xml.dom.minidom import Document


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
        doc = Document()
        element = doc.createElement("arg")
        element.setAttribute("name", self.name)

        if self.title is not None:
            title_element = doc.createElement("title")
            title_element.appendChild(doc.createTextNode(self.title))
            element.appendChild(title_element)

        if self.description is not None:
            description_element = doc.createElement("description")
            description_element.appendChild(
                doc.createTextNode(self.description))
            element.appendChild(description_element)

        if self.validation is not None:
            validation_element = doc.createElement("validation")
            validation_element.appendChild(doc.createTextNode(self.validation))
            element.appendChild(validation_element)

        data_type_element = doc.createElement("data_type")
        data_type_element.appendChild(doc.createTextNode(self.data_type))
        element.appendChild(data_type_element)

        required_on_edit_element = doc.createElement("required_on_edit")
        required_on_edit_element.appendChild(
            doc.createTextNode(str(self.required_on_edit).lower()))
        element.appendChild(required_on_edit_element)

        required_on_create_element = doc.createElement("required_on_create")
        required_on_create_element.appendChild(
            doc.createTextNode(str(self.required_on_create).lower()))
        element.appendChild(required_on_create_element)

        parent.appendChild(element)
