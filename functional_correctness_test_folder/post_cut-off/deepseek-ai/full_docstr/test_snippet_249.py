import snippet_249 as module_0

def test_case_0():
    str_0 = 'SyA`M\x0cqL;IS}$LFZ1'
    message_0 = module_0.Message(str_0, str_0)
    assert f'{type(message_0).__module__}.{type(message_0).__qualname__}' == 'snippet_249.Message'
    assert message_0.role == 'SyA`M\x0cqL;IS}$LFZ1'
    assert message_0.content == 'SyA`M\x0cqL;IS}$LFZ1'
    assert f'{type(module_0.Message.from_dict).__module__}.{type(module_0.Message.from_dict).__qualname__}' == 'builtins.method'

def test_case_1():
    str_0 = 'SyA`M\x0cqL;IS}$LFZ1'
    message_0 = module_0.Message(str_0, str_0)
    assert f'{type(message_0).__module__}.{type(message_0).__qualname__}' == 'snippet_249.Message'
    assert message_0.role == 'SyA`M\x0cqL;IS}$LFZ1'
    assert message_0.content == 'SyA`M\x0cqL;IS}$LFZ1'
    assert f'{type(module_0.Message.from_dict).__module__}.{type(module_0.Message.from_dict).__qualname__}' == 'builtins.method'
    message_0.to_dict()