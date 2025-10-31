import snippet_119 as module_0

def test_case_0():
    dummy_class_0 = module_0.DummyClass()
    assert f'{type(dummy_class_0).__module__}.{type(dummy_class_0).__qualname__}' == 'snippet_119.DummyClass'
    assert f'{type(module_0.DummyClass.prop).__module__}.{type(module_0.DummyClass.prop).__qualname__}' == 'builtins.property'
    dummy_class_0.run()