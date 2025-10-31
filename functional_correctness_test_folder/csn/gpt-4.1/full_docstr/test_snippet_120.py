import snippet_120 as module_0

def test_case_0():
    nested_dummy_class_0 = module_0.NestedDummyClass()
    assert f'{type(nested_dummy_class_0).__module__}.{type(nested_dummy_class_0).__qualname__}' == 'snippet_120.NestedDummyClass'
    assert f'{type(module_0.NestedDummyClass.prop).__module__}.{type(module_0.NestedDummyClass.prop).__qualname__}' == 'builtins.property'
    nested_dummy_class_0.run()