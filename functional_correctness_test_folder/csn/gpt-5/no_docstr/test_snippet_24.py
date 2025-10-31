import pytest
import snippet_24 as module_0
import subprocess as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = False
    set_0 = {bool_0, bool_0, bool_0, bool_0}
    app_0 = module_0.App(bool_0)
    assert f'{type(app_0).__module__}.{type(app_0).__qualname__}' == 'snippet_24.App'
    assert f'{type(app_0.runtime).__module__}.{type(app_0.runtime).__qualname__}' == 'ansible_compat.runtime.Runtime'
    assert f'{type(module_0.original_stderr).__module__}.{type(module_0.original_stderr).__qualname__}' == 'rich.file_proxy.FileProxy'
    app_1 = module_0.App(bool_0)
    assert f'{type(app_1).__module__}.{type(app_1).__qualname__}' == 'snippet_24.App'
    assert f'{type(app_1.runtime).__module__}.{type(app_1.runtime).__qualname__}' == 'ansible_compat.runtime.Runtime'
    app_2 = module_0.App(set_0)
    assert f'{type(app_2).__module__}.{type(app_2).__qualname__}' == 'snippet_24.App'
    assert f'{type(app_2.runtime).__module__}.{type(app_2.runtime).__qualname__}' == 'ansible_compat.runtime.Runtime'
    bool_1 = True
    bool_2 = False
    bool_3 = False
    app_0.run_command(app_1, app_2, debug=bool_1, echo=bool_2, quiet=bool_3)

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = '1CIz'
    bool_0 = True
    app_0 = module_0.App(str_0)
    assert f'{type(app_0).__module__}.{type(app_0).__qualname__}' == 'snippet_24.App'
    assert f'{type(app_0.runtime).__module__}.{type(app_0.runtime).__qualname__}' == 'ansible_compat.runtime.Runtime'
    assert f'{type(module_0.original_stderr).__module__}.{type(module_0.original_stderr).__qualname__}' == 'rich.file_proxy.FileProxy'
    float_0 = -3565.239
    app_1 = module_0.App(float_0)
    assert f'{type(app_1).__module__}.{type(app_1).__qualname__}' == 'snippet_24.App'
    assert f'{type(app_1.runtime).__module__}.{type(app_1.runtime).__qualname__}' == 'ansible_compat.runtime.Runtime'
    app_1.run_command(str_0, str_0, quiet=bool_0, check=app_0)

def test_case_2():
    str_0 = '>L.is'
    bool_0 = True
    none_type_0 = None
    bool_1 = True
    str_1 = 'F7L\x0cw\\,bN>`'
    app_0 = module_0.App(bool_0)
    assert f'{type(app_0).__module__}.{type(app_0).__qualname__}' == 'snippet_24.App'
    assert f'{type(app_0.runtime).__module__}.{type(app_0.runtime).__qualname__}' == 'ansible_compat.runtime.Runtime'
    assert f'{type(module_0.original_stderr).__module__}.{type(module_0.original_stderr).__qualname__}' == 'rich.file_proxy.FileProxy'
    completed_process_0 = app_0.run_command(str_0, none_type_0, debug=bool_1, command_borders=str_1)
    assert f'{type(completed_process_0).__module__}.{type(completed_process_0).__qualname__}' == 'subprocess.CompletedProcess'
    assert completed_process_0.args == '>L.is'
    assert completed_process_0.returncode == 0
    assert completed_process_0.stdout == ''
    assert completed_process_0.stderr == ''
    none_type_1 = None
    bytes_0 = b'b\xb3&\xebkB:\xfa\xfd\xf7\nu\xa5(\xbc\x96\xa3a'
    app_1 = module_0.App(bytes_0)
    assert f'{type(app_1).__module__}.{type(app_1).__qualname__}' == 'snippet_24.App'
    assert f'{type(app_1.runtime).__module__}.{type(app_1.runtime).__qualname__}' == 'ansible_compat.runtime.Runtime'
    completed_process_1 = app_1.run_command(str_0, echo=bool_0, quiet=none_type_1, command_borders=bool_0)
    assert f'{type(completed_process_1).__module__}.{type(completed_process_1).__qualname__}' == 'subprocess.CompletedProcess'
    assert completed_process_1.args == '>L.is'
    assert completed_process_1.returncode == 0
    assert completed_process_1.stdout == ''
    assert completed_process_1.stderr == ''

def test_case_3():
    none_type_0 = None
    app_0 = module_0.App(none_type_0)
    assert f'{type(app_0).__module__}.{type(app_0).__qualname__}' == 'snippet_24.App'
    assert f'{type(app_0.runtime).__module__}.{type(app_0.runtime).__qualname__}' == 'ansible_compat.runtime.Runtime'
    assert f'{type(module_0.original_stderr).__module__}.{type(module_0.original_stderr).__qualname__}' == 'rich.file_proxy.FileProxy'
    app_1 = module_0.App(none_type_0)
    assert f'{type(app_1).__module__}.{type(app_1).__qualname__}' == 'snippet_24.App'
    assert f'{type(app_1.runtime).__module__}.{type(app_1.runtime).__qualname__}' == 'ansible_compat.runtime.Runtime'
    str_0 = '|39)4AT!x\t\x0bPT^=XN_'
    str_1 = '\x0cPHg?FA\nDNa&\x0bu\r'
    with pytest.raises(module_1.CalledProcessError):
        app_1.run_command(str_0, quiet=str_1, check=app_0)

def test_case_4():
    bool_0 = True
    dict_0 = {bool_0: bool_0, bool_0: bool_0}
    app_0 = module_0.App(dict_0)
    assert f'{type(app_0).__module__}.{type(app_0).__qualname__}' == 'snippet_24.App'
    assert f'{type(app_0.runtime).__module__}.{type(app_0.runtime).__qualname__}' == 'ansible_compat.runtime.Runtime'
    assert f'{type(module_0.original_stderr).__module__}.{type(module_0.original_stderr).__qualname__}' == 'rich.file_proxy.FileProxy'

@pytest.mark.xfail(strict=True)
def test_case_5():
    str_0 = 'WyAO5[2D"'
    none_type_0 = None
    bool_0 = False
    set_0 = {str_0, str_0}
    app_0 = module_0.App(set_0)
    assert f'{type(app_0).__module__}.{type(app_0).__qualname__}' == 'snippet_24.App'
    assert f'{type(app_0.runtime).__module__}.{type(app_0.runtime).__qualname__}' == 'ansible_compat.runtime.Runtime'
    assert f'{type(module_0.original_stderr).__module__}.{type(module_0.original_stderr).__qualname__}' == 'rich.file_proxy.FileProxy'
    completed_process_0 = app_0.run_command(str_0, none_type_0, echo=str_0, quiet=bool_0)
    assert f'{type(completed_process_0).__module__}.{type(completed_process_0).__qualname__}' == 'subprocess.CompletedProcess'
    assert completed_process_0.args == 'WyAO5[2D"'
    assert completed_process_0.returncode == 2
    assert completed_process_0.stdout == ''
    assert completed_process_0.stderr == '/bin/sh: -c: line 0: unexpected EOF while looking for matching `"\'\n/bin/sh: -c: line 1: syntax error: unexpected end of file\n'
    str_1 = 'KpE%'
    str_2 = '`u;(3 \x0bmi5S3J)\n'
    list_0 = [str_0, str_1, str_2]
    bool_1 = False
    none_type_1 = None
    app_1 = module_0.App(none_type_1)
    assert f'{type(app_1).__module__}.{type(app_1).__qualname__}' == 'snippet_24.App'
    assert f'{type(app_1.runtime).__module__}.{type(app_1.runtime).__qualname__}' == 'ansible_compat.runtime.Runtime'
    app_1.run_command(list_0, debug=str_0, command_borders=bool_1)