
import xml.etree.ElementTree as ET


class Argument:
    '''Class representing an argument for a modular input kind.'''

    def __init__(self, name, title, description, data_type='string', required_on_create=False, required_on_edit=False):
        '''
        :param name: ``string`` name of the argument.
        :param title: ``string`` title of the argument.
        :param description: ``string`` description of the argument.
        :param data_type: ``string`` data type of the argument. Defaults to 'string'.
        :param required_on_create: ``bool`` whether the argument is required on create. Defaults to False.
        :param required_on_edit: ``bool`` whether the argument is required on edit. Defaults to False.
        '''
        self.name = name
        self.title = title
        self.description = description
        self.data_type = data_type
        self.required_on_create = required_on_create
        self.required_on_edit = required_on_edit


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
        self.description = None
        self.use_external_validation = True
        self.streaming_mode = 'xml'
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
        root = ET.Element('scheme')

        ET.SubElement(root, 'title').text = self.title

        if self.description is not None:
            ET.SubElement(root, 'description').text = self.description

        ET.SubElement(root, 'use_external_validation').text = str(
            self.use_external_validation).lower()
        ET.SubElement(root, 'streaming_mode').text = self.streaming_mode
        ET.SubElement(root, 'use_single_instance').text = str(
            self.use_single_instance).lower()

        args_element = ET.SubElement(root, 'endpoint')
        args_element.set('name', 'configs/conf-myapp')

        args_list_element = ET.SubElement(args_element, 'args')

        for arg in self.arguments:
            arg_element = ET.SubElement(args_list_element, 'arg')
            arg_element.set('name', arg.name)

            ET.SubElement(arg_element, 'title').text = arg.title
            ET.SubElement(arg_element, 'description').text = arg.description
            ET.SubElement(arg_element, 'data_type').text = arg.data_type
            ET.SubElement(arg_element, 'required_on_create').text = str(
                arg.required_on_create).lower()
            ET.SubElement(arg_element, 'required_on_edit').text = str(
                arg.required_on_edit).lower()

        return root


# Example usage:
if __name__ == "__main__":
    scheme = Scheme('My Modular Input')
    scheme.description = 'This is a modular input.'
    scheme.use_external_validation = True
    scheme.streaming_mode = 'xml'
    scheme.use_single_instance = False

    arg1 = Argument('arg1', 'Argument 1', 'This is argument 1.')
    arg2 = Argument('arg2', 'Argument 2', 'This is argument 2.',
                    required_on_create=True)

    scheme.add_argument(arg1)
    scheme.add_argument(arg2)

    xml = scheme.to_xml()
    ET.indent(xml, space='\t', level=0)
    print(ET.tostring(xml, encoding='unicode'))
