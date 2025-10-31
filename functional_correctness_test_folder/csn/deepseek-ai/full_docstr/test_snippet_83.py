import snippet_83 as module_0
import xml.etree.ElementTree as module_1

def test_case_0():
    none_type_0 = None
    argument_0 = module_0.Argument(none_type_0, none_type_0)
    assert f'{type(argument_0).__module__}.{type(argument_0).__qualname__}' == 'snippet_83.Argument'
    assert argument_0.name is None
    assert argument_0.description is None
    assert argument_0.validation is None
    assert argument_0.data_type == 'STRING'
    assert argument_0.required_on_edit is False
    assert argument_0.required_on_create is False
    assert argument_0.title is None
    assert module_0.Argument.data_type_boolean == 'BOOLEAN'
    assert module_0.Argument.data_type_number == 'NUMBER'
    assert module_0.Argument.data_type_string == 'STRING'

def test_case_1():
    var_0 = module_1.Comment()
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(var_0) == 0
    assert module_1.VERSION == '1.3.0'
    assert module_1.HTML_EMPTY == {'hr', 'img', 'meta', 'col', 'frame', 'isindex', 'area', 'param', 'base', 'basefont', 'input', 'link', 'br'}
    assert f'{type(module_1.Element.tag).__module__}.{type(module_1.Element.tag).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.text).__module__}.{type(module_1.Element.text).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.tail).__module__}.{type(module_1.Element.tail).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.attrib).__module__}.{type(module_1.Element.attrib).__qualname__}' == 'builtins.getset_descriptor'
    argument_0 = module_0.Argument(var_0, required_on_edit=var_0)
    assert f'{type(argument_0).__module__}.{type(argument_0).__qualname__}' == 'snippet_83.Argument'
    assert f'{type(argument_0.name).__module__}.{type(argument_0.name).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_0.name) == 0
    assert argument_0.description is None
    assert argument_0.validation is None
    assert argument_0.data_type == 'STRING'
    assert f'{type(argument_0.required_on_edit).__module__}.{type(argument_0.required_on_edit).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_0.required_on_edit) == 0
    assert argument_0.required_on_create is False
    assert argument_0.title is None
    assert module_0.Argument.data_type_boolean == 'BOOLEAN'
    assert module_0.Argument.data_type_number == 'NUMBER'
    assert module_0.Argument.data_type_string == 'STRING'
    var_1 = argument_0.add_to_document(var_0)
    assert len(var_0) == 1
    assert len(argument_0.name) == 1
    assert len(argument_0.required_on_edit) == 1
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(var_1) == 3

def test_case_2():
    var_0 = module_1.Comment()
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(var_0) == 0
    assert module_1.VERSION == '1.3.0'
    assert module_1.HTML_EMPTY == {'hr', 'img', 'meta', 'col', 'frame', 'isindex', 'area', 'param', 'base', 'basefont', 'input', 'link', 'br'}
    assert f'{type(module_1.Element.tag).__module__}.{type(module_1.Element.tag).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.text).__module__}.{type(module_1.Element.text).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.tail).__module__}.{type(module_1.Element.tail).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.attrib).__module__}.{type(module_1.Element.attrib).__qualname__}' == 'builtins.getset_descriptor'
    argument_0 = module_0.Argument(var_0, var_0, required_on_create=var_0)
    assert f'{type(argument_0).__module__}.{type(argument_0).__qualname__}' == 'snippet_83.Argument'
    assert f'{type(argument_0.name).__module__}.{type(argument_0.name).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_0.name) == 0
    assert f'{type(argument_0.description).__module__}.{type(argument_0.description).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_0.description) == 0
    assert argument_0.validation is None
    assert argument_0.data_type == 'STRING'
    assert argument_0.required_on_edit is False
    assert f'{type(argument_0.required_on_create).__module__}.{type(argument_0.required_on_create).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_0.required_on_create) == 0
    assert argument_0.title is None
    assert module_0.Argument.data_type_boolean == 'BOOLEAN'
    assert module_0.Argument.data_type_number == 'NUMBER'
    assert module_0.Argument.data_type_string == 'STRING'
    var_1 = argument_0.add_to_document(var_0)
    assert len(var_0) == 1
    assert len(argument_0.name) == 1
    assert len(argument_0.description) == 1
    assert len(argument_0.required_on_create) == 1
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(var_1) == 4

def test_case_3():
    var_0 = module_1.Comment()
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(var_0) == 0
    assert module_1.VERSION == '1.3.0'
    assert module_1.HTML_EMPTY == {'hr', 'img', 'meta', 'col', 'frame', 'isindex', 'area', 'param', 'base', 'basefont', 'input', 'link', 'br'}
    assert f'{type(module_1.Element.tag).__module__}.{type(module_1.Element.tag).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.text).__module__}.{type(module_1.Element.text).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.tail).__module__}.{type(module_1.Element.tail).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.attrib).__module__}.{type(module_1.Element.attrib).__qualname__}' == 'builtins.getset_descriptor'
    argument_0 = module_0.Argument(var_0, var_0, required_on_create=var_0)
    assert f'{type(argument_0).__module__}.{type(argument_0).__qualname__}' == 'snippet_83.Argument'
    assert f'{type(argument_0.name).__module__}.{type(argument_0.name).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_0.name) == 0
    assert f'{type(argument_0.description).__module__}.{type(argument_0.description).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_0.description) == 0
    assert argument_0.validation is None
    assert argument_0.data_type == 'STRING'
    assert argument_0.required_on_edit is False
    assert f'{type(argument_0.required_on_create).__module__}.{type(argument_0.required_on_create).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_0.required_on_create) == 0
    assert argument_0.title is None
    assert module_0.Argument.data_type_boolean == 'BOOLEAN'
    assert module_0.Argument.data_type_number == 'NUMBER'
    assert module_0.Argument.data_type_string == 'STRING'
    argument_1 = module_0.Argument(argument_0, title=argument_0)
    assert f'{type(argument_1).__module__}.{type(argument_1).__qualname__}' == 'snippet_83.Argument'
    assert f'{type(argument_1.name).__module__}.{type(argument_1.name).__qualname__}' == 'snippet_83.Argument'
    assert argument_1.description is None
    assert argument_1.validation is None
    assert argument_1.data_type == 'STRING'
    assert argument_1.required_on_edit is False
    assert argument_1.required_on_create is False
    assert f'{type(argument_1.title).__module__}.{type(argument_1.title).__qualname__}' == 'snippet_83.Argument'
    var_1 = argument_1.add_to_document(var_0)
    assert len(var_0) == 1
    assert len(argument_0.name) == 1
    assert len(argument_0.description) == 1
    assert len(argument_0.required_on_create) == 1
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(var_1) == 4

def test_case_4():
    var_0 = module_1.Comment()
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(var_0) == 0
    assert module_1.VERSION == '1.3.0'
    assert module_1.HTML_EMPTY == {'hr', 'img', 'meta', 'col', 'frame', 'isindex', 'area', 'param', 'base', 'basefont', 'input', 'link', 'br'}
    assert f'{type(module_1.Element.tag).__module__}.{type(module_1.Element.tag).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.text).__module__}.{type(module_1.Element.text).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.tail).__module__}.{type(module_1.Element.tail).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.attrib).__module__}.{type(module_1.Element.attrib).__qualname__}' == 'builtins.getset_descriptor'
    var_1 = module_1.Comment()
    assert f'{type(var_1).__module__}.{type(var_1).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(var_1) == 0
    argument_0 = module_0.Argument(var_0, validation=var_0, data_type=var_0, required_on_edit=var_1)
    assert f'{type(argument_0).__module__}.{type(argument_0).__qualname__}' == 'snippet_83.Argument'
    assert f'{type(argument_0.name).__module__}.{type(argument_0.name).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_0.name) == 0
    assert argument_0.description is None
    assert f'{type(argument_0.validation).__module__}.{type(argument_0.validation).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_0.validation) == 0
    assert f'{type(argument_0.data_type).__module__}.{type(argument_0.data_type).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_0.data_type) == 0
    assert f'{type(argument_0.required_on_edit).__module__}.{type(argument_0.required_on_edit).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_0.required_on_edit) == 0
    assert argument_0.required_on_create is False
    assert argument_0.title is None
    assert module_0.Argument.data_type_boolean == 'BOOLEAN'
    assert module_0.Argument.data_type_number == 'NUMBER'
    assert module_0.Argument.data_type_string == 'STRING'
    argument_1 = module_0.Argument(var_0, var_0, required_on_create=argument_0)
    assert f'{type(argument_1).__module__}.{type(argument_1).__qualname__}' == 'snippet_83.Argument'
    assert f'{type(argument_1.name).__module__}.{type(argument_1.name).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_1.name) == 0
    assert f'{type(argument_1.description).__module__}.{type(argument_1.description).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(argument_1.description) == 0
    assert argument_1.validation is None
    assert argument_1.data_type == 'STRING'
    assert argument_1.required_on_edit is False
    assert f'{type(argument_1.required_on_create).__module__}.{type(argument_1.required_on_create).__qualname__}' == 'snippet_83.Argument'
    assert argument_1.title is None
    var_2 = argument_1.add_to_document(var_0)
    assert len(var_0) == 1
    assert len(argument_0.name) == 1
    assert len(argument_0.validation) == 1
    assert len(argument_0.data_type) == 1
    assert len(argument_1.name) == 1
    assert len(argument_1.description) == 1
    assert f'{type(var_2).__module__}.{type(var_2).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(var_2) == 4
    var_3 = argument_0.add_to_document(var_1)
    assert len(var_1) == 1
    assert len(argument_0.required_on_edit) == 1
    assert f'{type(var_3).__module__}.{type(var_3).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(var_3) == 4