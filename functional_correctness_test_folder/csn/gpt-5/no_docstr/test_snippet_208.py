import snippet_208 as module_0
import _io as module_1

def test_case_0():
    null_file_0 = module_0.NullFile()
    assert null_file_0.mode == 'w'
    assert f'{type(module_1.TextIOWrapper.encoding).__module__}.{type(module_1.TextIOWrapper.encoding).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.TextIOWrapper.buffer).__module__}.{type(module_1.TextIOWrapper.buffer).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.TextIOWrapper.line_buffering).__module__}.{type(module_1.TextIOWrapper.line_buffering).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.TextIOWrapper.write_through).__module__}.{type(module_1.TextIOWrapper.write_through).__qualname__}' == 'builtins.member_descriptor'
    assert f'{type(module_1.TextIOWrapper.name).__module__}.{type(module_1.TextIOWrapper.name).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.TextIOWrapper.closed).__module__}.{type(module_1.TextIOWrapper.closed).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.TextIOWrapper.newlines).__module__}.{type(module_1.TextIOWrapper.newlines).__qualname__}' == 'builtins.getset_descriptor'
    assert f'{type(module_1.TextIOWrapper.errors).__module__}.{type(module_1.TextIOWrapper.errors).__qualname__}' == 'builtins.getset_descriptor'