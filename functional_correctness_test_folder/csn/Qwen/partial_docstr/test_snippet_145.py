import pytest
import snippet_145 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    int_0 = 603
    method_doc_descriptor_0 = module_0._MethodDocDescriptor(int_0, int_0, int_0)
    assert f'{type(method_doc_descriptor_0).__module__}.{type(method_doc_descriptor_0).__qualname__}' == 'snippet_145._MethodDocDescriptor'
    assert method_doc_descriptor_0.ref == 603
    assert method_doc_descriptor_0.class_name == 603
    assert method_doc_descriptor_0.name == 603
    assert method_doc_descriptor_0.doc is None
    method_doc_descriptor_0.__get__(method_doc_descriptor_0)

def test_case_1():
    int_0 = 603
    method_doc_descriptor_0 = module_0._MethodDocDescriptor(int_0, int_0, int_0)
    assert f'{type(method_doc_descriptor_0).__module__}.{type(method_doc_descriptor_0).__qualname__}' == 'snippet_145._MethodDocDescriptor'
    assert method_doc_descriptor_0.ref == 603
    assert method_doc_descriptor_0.class_name == 603
    assert method_doc_descriptor_0.name == 603
    assert method_doc_descriptor_0.doc is None