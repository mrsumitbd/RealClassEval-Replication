import snippet_20 as module_0

def test_case_0():
    str_0 = 'lg<!huZ&}0NEvmW'
    m_c_p_resource_0 = module_0.MCPResource(str_0, str_0, str_0, str_0)
    assert f'{type(m_c_p_resource_0).__module__}.{type(m_c_p_resource_0).__qualname__}' == 'snippet_20.MCPResource'
    assert m_c_p_resource_0.uri == 'lg<!huZ&}0NEvmW'
    assert m_c_p_resource_0.name == 'lg<!huZ&}0NEvmW'
    assert m_c_p_resource_0.description == 'lg<!huZ&}0NEvmW'
    assert m_c_p_resource_0.mime_type == 'lg<!huZ&}0NEvmW'
    assert module_0.MCPResource.mime_type is None
    assert f'{type(module_0.MCPResource.from_dict).__module__}.{type(module_0.MCPResource.from_dict).__qualname__}' == 'builtins.method'
    m_c_p_resource_0.to_dict()

def test_case_1():
    str_0 = '`\\Ni'
    str_1 = ''
    m_c_p_resource_0 = module_0.MCPResource(str_0, str_0, str_1, str_0)
    assert f'{type(m_c_p_resource_0).__module__}.{type(m_c_p_resource_0).__qualname__}' == 'snippet_20.MCPResource'
    assert m_c_p_resource_0.uri == '`\\Ni'
    assert m_c_p_resource_0.name == '`\\Ni'
    assert m_c_p_resource_0.description == ''
    assert m_c_p_resource_0.mime_type == '`\\Ni'
    assert module_0.MCPResource.mime_type is None
    assert f'{type(module_0.MCPResource.from_dict).__module__}.{type(module_0.MCPResource.from_dict).__qualname__}' == 'builtins.method'
    str_2 = 'z8 (LJ8=4\rc8#Kb|'
    m_c_p_resource_0.to_dict()
    m_c_p_resource_1 = module_0.MCPResource(str_0, str_1, str_2)
    assert f'{type(m_c_p_resource_1).__module__}.{type(m_c_p_resource_1).__qualname__}' == 'snippet_20.MCPResource'
    assert m_c_p_resource_1.uri == '`\\Ni'
    assert m_c_p_resource_1.name == ''
    assert m_c_p_resource_1.description == 'z8 (LJ8=4\rc8#Kb|'
    assert m_c_p_resource_1.mime_type is None
    m_c_p_resource_1.to_dict()