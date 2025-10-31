import pytest
import snippet_339 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = 'q>PBZ3"L-=k"Iognk'
    m_c_p_config_generator_0 = module_0.MCPConfigGenerator(str_0)
    assert f'{type(m_c_p_config_generator_0).__module__}.{type(m_c_p_config_generator_0).__qualname__}' == 'snippet_339.MCPConfigGenerator'
    assert m_c_p_config_generator_0.base_dir == 'q>PBZ3"L-=k"Iognk'
    dict_0 = {}
    dict_1 = m_c_p_config_generator_0.generate_config(dict_0)
    m_c_p_config_generator_0.generate_config(dict_1)

def test_case_1():
    m_c_p_config_generator_0 = module_0.MCPConfigGenerator()
    assert f'{type(m_c_p_config_generator_0).__module__}.{type(m_c_p_config_generator_0).__qualname__}' == 'snippet_339.MCPConfigGenerator'
    assert m_c_p_config_generator_0.base_dir == '/Users/musfiqurrahman/Documents/MISC/pynguin_expt'