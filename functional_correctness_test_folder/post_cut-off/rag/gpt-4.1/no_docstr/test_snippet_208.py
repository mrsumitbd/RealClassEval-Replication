import pytest
import snippet_208 as module_0

def test_case_0():
    option_r_o_m_manager_0 = module_0.OptionROMManager()
    assert f'{type(option_r_o_m_manager_0).__module__}.{type(option_r_o_m_manager_0).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_0.output_dir).__module__}.{type(option_r_o_m_manager_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_0.rom_file_path is None
    assert option_r_o_m_manager_0.rom_size == 0
    assert option_r_o_m_manager_0.rom_data is None

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = 'E\x0b'
    option_r_o_m_manager_0 = module_0.OptionROMManager(rom_file_path=str_0)
    assert f'{type(option_r_o_m_manager_0).__module__}.{type(option_r_o_m_manager_0).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_0.output_dir).__module__}.{type(option_r_o_m_manager_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_0.rom_file_path == 'E\x0b'
    assert option_r_o_m_manager_0.rom_size == 0
    assert option_r_o_m_manager_0.rom_data is None
    option_r_o_m_manager_1 = module_0.OptionROMManager(str_0)
    assert f'{type(option_r_o_m_manager_1).__module__}.{type(option_r_o_m_manager_1).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_1.output_dir).__module__}.{type(option_r_o_m_manager_1.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_1.rom_file_path is None
    assert option_r_o_m_manager_1.rom_size == 0
    assert option_r_o_m_manager_1.rom_data is None
    option_r_o_m_manager_1.setup_option_rom(option_r_o_m_manager_1, option_r_o_m_manager_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = '=  '
    option_r_o_m_manager_0 = module_0.OptionROMManager()
    assert f'{type(option_r_o_m_manager_0).__module__}.{type(option_r_o_m_manager_0).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_0.output_dir).__module__}.{type(option_r_o_m_manager_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_0.rom_file_path is None
    assert option_r_o_m_manager_0.rom_size == 0
    assert option_r_o_m_manager_0.rom_data is None
    option_r_o_m_manager_0.extract_rom_linux(str_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    option_r_o_m_manager_0 = module_0.OptionROMManager()
    assert f'{type(option_r_o_m_manager_0).__module__}.{type(option_r_o_m_manager_0).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_0.output_dir).__module__}.{type(option_r_o_m_manager_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_0.rom_file_path is None
    assert option_r_o_m_manager_0.rom_size == 0
    assert option_r_o_m_manager_0.rom_data is None
    option_r_o_m_manager_0.setup_option_rom(option_r_o_m_manager_0)

@pytest.mark.xfail(strict=True)
def test_case_4():
    option_r_o_m_manager_0 = module_0.OptionROMManager()
    assert f'{type(option_r_o_m_manager_0).__module__}.{type(option_r_o_m_manager_0).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_0.output_dir).__module__}.{type(option_r_o_m_manager_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_0.rom_file_path is None
    assert option_r_o_m_manager_0.rom_size == 0
    assert option_r_o_m_manager_0.rom_data is None
    option_r_o_m_manager_0.load_rom_file()

@pytest.mark.xfail(strict=True)
def test_case_5():
    option_r_o_m_manager_0 = module_0.OptionROMManager()
    assert f'{type(option_r_o_m_manager_0).__module__}.{type(option_r_o_m_manager_0).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_0.output_dir).__module__}.{type(option_r_o_m_manager_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_0.rom_file_path is None
    assert option_r_o_m_manager_0.rom_size == 0
    assert option_r_o_m_manager_0.rom_data is None
    option_r_o_m_manager_0.save_rom_hex()

@pytest.mark.xfail(strict=True)
def test_case_6():
    str_0 = 'E'
    option_r_o_m_manager_0 = module_0.OptionROMManager(rom_file_path=str_0)
    assert f'{type(option_r_o_m_manager_0).__module__}.{type(option_r_o_m_manager_0).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_0.output_dir).__module__}.{type(option_r_o_m_manager_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_0.rom_file_path == 'E'
    assert option_r_o_m_manager_0.rom_size == 0
    assert option_r_o_m_manager_0.rom_data is None
    option_r_o_m_manager_1 = module_0.OptionROMManager(str_0)
    assert f'{type(option_r_o_m_manager_1).__module__}.{type(option_r_o_m_manager_1).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_1.output_dir).__module__}.{type(option_r_o_m_manager_1.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_1.rom_file_path is None
    assert option_r_o_m_manager_1.rom_size == 0
    assert option_r_o_m_manager_1.rom_data is None
    option_r_o_m_manager_0.get_rom_info()

def test_case_7():
    str_0 = 'E\x0b'
    option_r_o_m_manager_0 = module_0.OptionROMManager(str_0)
    assert f'{type(option_r_o_m_manager_0).__module__}.{type(option_r_o_m_manager_0).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_0.output_dir).__module__}.{type(option_r_o_m_manager_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_0.rom_file_path is None
    assert option_r_o_m_manager_0.rom_size == 0
    assert option_r_o_m_manager_0.rom_data is None
    option_r_o_m_manager_0.get_rom_info()

@pytest.mark.xfail(strict=True)
def test_case_8():
    str_0 = 'E\x0b'
    option_r_o_m_manager_0 = module_0.OptionROMManager(str_0)
    assert f'{type(option_r_o_m_manager_0).__module__}.{type(option_r_o_m_manager_0).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_0.output_dir).__module__}.{type(option_r_o_m_manager_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_0.rom_file_path is None
    assert option_r_o_m_manager_0.rom_size == 0
    assert option_r_o_m_manager_0.rom_data is None
    str_1 = 'V'
    option_r_o_m_manager_0.get_rom_info()
    none_type_0 = None
    option_r_o_m_manager_1 = module_0.OptionROMManager(rom_file_path=none_type_0)
    assert f'{type(option_r_o_m_manager_1).__module__}.{type(option_r_o_m_manager_1).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_1.output_dir).__module__}.{type(option_r_o_m_manager_1.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_1.rom_file_path is None
    assert option_r_o_m_manager_1.rom_size == 0
    assert option_r_o_m_manager_1.rom_data is None
    option_r_o_m_manager_1.load_rom_file(str_1)

@pytest.mark.xfail(strict=True)
def test_case_9():
    str_0 = 'E\x0b'
    option_r_o_m_manager_0 = module_0.OptionROMManager(rom_file_path=str_0)
    assert f'{type(option_r_o_m_manager_0).__module__}.{type(option_r_o_m_manager_0).__qualname__}' == 'snippet_208.OptionROMManager'
    assert f'{type(option_r_o_m_manager_0.output_dir).__module__}.{type(option_r_o_m_manager_0.output_dir).__qualname__}' == 'pathlib.PosixPath'
    assert option_r_o_m_manager_0.rom_file_path == 'E\x0b'
    assert option_r_o_m_manager_0.rom_size == 0
    assert option_r_o_m_manager_0.rom_data is None
    option_r_o_m_manager_0.setup_option_rom(option_r_o_m_manager_0, option_r_o_m_manager_0)