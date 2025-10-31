import snippet_86 as module_0

def test_case_0():
    bytes_0 = b'\xd8\x81\xd0o\xcah\xdfU8q\x9b\x94\x0b\xe6'
    cmd2_attribute_wrapper_0 = module_0.Cmd2AttributeWrapper(bytes_0)
    assert f'{type(cmd2_attribute_wrapper_0).__module__}.{type(cmd2_attribute_wrapper_0).__qualname__}' == 'snippet_86.Cmd2AttributeWrapper'
    assert module_0.TYPE_CHECKING is False
    var_0 = cmd2_attribute_wrapper_0.get()
    assert var_0 == b'\xd8\x81\xd0o\xcah\xdfU8q\x9b\x94\x0b\xe6'
    cmd2_attribute_wrapper_0.set(var_0)