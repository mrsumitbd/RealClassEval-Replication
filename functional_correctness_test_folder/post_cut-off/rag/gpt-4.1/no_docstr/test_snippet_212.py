import pytest
import snippet_212 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = True
    module_0.VivadoRunner(bool_0, bool_0, bool_0, bool_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = False
    module_0.VivadoRunner(bool_0, bool_0, bool_0, bool_0)

def test_case_2():
    str_0 = 'Ql'
    vivado_runner_0 = module_0.VivadoRunner(str_0, str_0, str_0, str_0)
    assert f'{type(vivado_runner_0).__module__}.{type(vivado_runner_0).__qualname__}' == 'snippet_212.VivadoRunner'
    assert vivado_runner_0.logger == 'Ql'
    assert vivado_runner_0.board == 'Ql'
    assert f'{type(vivado_runner_0.output_dir).__module__}.{type(vivado_runner_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert vivado_runner_0.vivado_path == 'Ql'
    assert vivado_runner_0.device_config is None
    assert vivado_runner_0.vivado_executable == 'Ql/bin/vivado'
    assert vivado_runner_0.vivado_bin_dir == 'Ql/bin'
    assert vivado_runner_0.vivado_version == 'unknown'

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = 'Ql'
    vivado_runner_0 = module_0.VivadoRunner(str_0, str_0, str_0, str_0)
    assert f'{type(vivado_runner_0).__module__}.{type(vivado_runner_0).__qualname__}' == 'snippet_212.VivadoRunner'
    assert vivado_runner_0.logger == 'Ql'
    assert vivado_runner_0.board == 'Ql'
    assert f'{type(vivado_runner_0.output_dir).__module__}.{type(vivado_runner_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert vivado_runner_0.vivado_path == 'Ql'
    assert vivado_runner_0.device_config is None
    assert vivado_runner_0.vivado_executable == 'Ql/bin/vivado'
    assert vivado_runner_0.vivado_bin_dir == 'Ql/bin'
    assert vivado_runner_0.vivado_version == 'unknown'
    vivado_runner_0.run()

@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = 'O'
    vivado_runner_0 = module_0.VivadoRunner(str_0, str_0, str_0, str_0)
    assert f'{type(vivado_runner_0).__module__}.{type(vivado_runner_0).__qualname__}' == 'snippet_212.VivadoRunner'
    assert vivado_runner_0.logger == 'O'
    assert vivado_runner_0.board == 'O'
    assert f'{type(vivado_runner_0.output_dir).__module__}.{type(vivado_runner_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert vivado_runner_0.vivado_path == 'O'
    assert vivado_runner_0.device_config is None
    assert vivado_runner_0.vivado_executable == 'O/bin/vivado'
    assert vivado_runner_0.vivado_bin_dir == 'O/bin'
    assert vivado_runner_0.vivado_version == 'unknown'
    vivado_runner_0.get_vivado_info()
    vivado_runner_0.run()