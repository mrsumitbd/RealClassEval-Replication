import pytest
import snippet_210 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    shell_0 = module_0.Shell()
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is False
    assert shell_0.safe_mode is True
    shell_0.run_check()

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = "oZKz,K'\nm"
    bool_0 = False
    shell_0 = module_0.Shell(safe_mode=bool_0)
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is False
    assert shell_0.safe_mode is False
    shell_0.run_check(timeout=str_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    none_type_0 = None
    bool_0 = True
    shell_0 = module_0.Shell(bool_0)
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is True
    assert shell_0.safe_mode is True
    shell_0.run(timeout=none_type_0, cwd=none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    bool_0 = False
    str_0 = "]*q*O \r\nl\rM2AS*?0'"
    list_0 = [str_0]
    bool_1 = True
    shell_0 = module_0.Shell(safe_mode=bool_1)
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is False
    assert shell_0.safe_mode is True
    shell_0.run_check(*list_0, cwd=bool_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    none_type_0 = None
    bool_0 = True
    shell_0 = module_0.Shell(safe_mode=bool_0)
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is False
    assert shell_0.safe_mode is True
    shell_1 = module_0.Shell(bool_0)
    assert f'{type(shell_1).__module__}.{type(shell_1).__qualname__}' == 'snippet_210.Shell'
    assert shell_1.dry_run is True
    assert shell_1.safe_mode is True
    str_0 = 'SfHIG%q7'
    list_0 = [str_0, str_0]
    list_1 = [none_type_0, none_type_0, none_type_0]
    bool_1 = shell_1.run_check(*list_1)
    assert bool_1 is False
    shell_0.run(*list_0, cwd=none_type_0)

@pytest.mark.xfail(strict=True)
def test_case_5():
    int_0 = -647
    complex_0 = -1180 + 599.583j
    bool_0 = False
    bool_1 = True
    shell_0 = module_0.Shell(bool_1)
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is True
    assert shell_0.safe_mode is True
    shell_0.write_file(int_0, complex_0, create_dirs=bool_0, permissions=bool_0)

@pytest.mark.xfail(strict=True)
def test_case_6():
    none_type_0 = None
    shell_0 = module_0.Shell()
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is False
    assert shell_0.safe_mode is True
    shell_0.write_file(none_type_0, none_type_0, none_type_0, permissions=none_type_0)

def test_case_7():
    shell_0 = module_0.Shell()
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is False
    assert shell_0.safe_mode is True

@pytest.mark.xfail(strict=True)
def test_case_8():
    shell_0 = module_0.Shell()
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is False
    assert shell_0.safe_mode is True
    str_0 = 'mk.+#T\tQ!V!'
    shell_0.write_file(str_0, shell_0)

@pytest.mark.xfail(strict=True)
def test_case_9():
    shell_0 = module_0.Shell()
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is False
    assert shell_0.safe_mode is True
    bool_0 = True
    str_0 = '2"!E)@'
    str_1 = '*-a5W'
    bool_1 = False
    shell_0.write_file(str_0, str_1, create_dirs=bool_1, permissions=bool_0)

@pytest.mark.xfail(strict=True)
def test_case_10():
    shell_0 = module_0.Shell()
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is False
    assert shell_0.safe_mode is True
    str_0 = '`a'
    bool_0 = False
    shell_1 = module_0.Shell()
    assert f'{type(shell_1).__module__}.{type(shell_1).__qualname__}' == 'snippet_210.Shell'
    assert shell_1.dry_run is False
    assert shell_1.safe_mode is True
    shell_1.write_file(str_0, shell_0, create_dirs=bool_0, permissions=bool_0)

@pytest.mark.xfail(strict=True)
def test_case_11():
    str_0 = '#H?z/AivVk:Fh'
    shell_0 = module_0.Shell()
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is False
    assert shell_0.safe_mode is True
    shell_0.write_file(str_0, str_0)

@pytest.mark.xfail(strict=True)
def test_case_12():
    str_0 = ''
    shell_0 = module_0.Shell()
    assert f'{type(shell_0).__module__}.{type(shell_0).__qualname__}' == 'snippet_210.Shell'
    assert shell_0.dry_run is False
    assert shell_0.safe_mode is True
    str_1 = 'iK'
    shell_0.write_file(str_0, str_1)