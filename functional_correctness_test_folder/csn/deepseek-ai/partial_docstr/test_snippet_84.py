import pytest
import snippet_84 as module_0
import xml.etree.ElementTree as module_1

def test_case_0():
    none_type_0 = None
    scheme_0 = module_0.Scheme(none_type_0)
    assert f'{type(scheme_0).__module__}.{type(scheme_0).__qualname__}' == 'snippet_84.Scheme'
    assert scheme_0.title is None
    assert scheme_0.description is None
    assert scheme_0.use_external_validation is True
    assert scheme_0.use_single_instance is False
    assert scheme_0.streaming_mode == 'XML'
    assert scheme_0.arguments == []
    assert module_0.Scheme.streaming_mode_simple == 'SIMPLE'
    assert module_0.Scheme.streaming_mode_xml == 'XML'
    var_0 = scheme_0.to_xml()
    assert f'{type(var_0).__module__}.{type(var_0).__qualname__}' == 'xml.etree.ElementTree.Element'
    assert len(var_0) == 5
    assert f'{type(module_1.Element.tag).__module__}.{type(module_1.Element.tag).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.text).__module__}.{type(module_1.Element.text).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.tail).__module__}.{type(module_1.Element.tail).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.Element.attrib).__module__}.{type(module_1.Element.attrib).__qualname__}' == 'builtins.getset_descriptor'

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    scheme_0 = module_0.Scheme(none_type_0)
    assert f'{type(scheme_0).__module__}.{type(scheme_0).__qualname__}' == 'snippet_84.Scheme'
    assert scheme_0.title is None
    assert scheme_0.description is None
    assert scheme_0.use_external_validation is True
    assert scheme_0.use_single_instance is False
    assert scheme_0.streaming_mode == 'XML'
    assert scheme_0.arguments == []
    assert module_0.Scheme.streaming_mode_simple == 'SIMPLE'
    assert module_0.Scheme.streaming_mode_xml == 'XML'
    var_0 = scheme_0.add_argument(scheme_0)
    assert f'{type(scheme_0.arguments).__module__}.{type(scheme_0.arguments).__qualname__}' == 'builtins.list'
    assert len(scheme_0.arguments) == 1
    scheme_0.to_xml()

def test_case_2():
    none_type_0 = None
    scheme_0 = module_0.Scheme(none_type_0)
    assert f'{type(scheme_0).__module__}.{type(scheme_0).__qualname__}' == 'snippet_84.Scheme'
    assert scheme_0.title is None
    assert scheme_0.description is None
    assert scheme_0.use_external_validation is True
    assert scheme_0.use_single_instance is False
    assert scheme_0.streaming_mode == 'XML'
    assert scheme_0.arguments == []
    assert module_0.Scheme.streaming_mode_simple == 'SIMPLE'
    assert module_0.Scheme.streaming_mode_xml == 'XML'