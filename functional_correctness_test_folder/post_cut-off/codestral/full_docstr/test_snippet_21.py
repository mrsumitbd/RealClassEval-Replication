import snippet_21 as module_0

def test_case_0():
    str_0 = 'A{{A:VC/'
    m_c_p_tool_0 = module_0.MCPTool(str_0, str_0, str_0)
    assert f'{type(m_c_p_tool_0).__module__}.{type(m_c_p_tool_0).__qualname__}' == 'snippet_21.MCPTool'
    assert m_c_p_tool_0.name == 'A{{A:VC/'
    assert m_c_p_tool_0.description == 'A{{A:VC/'
    assert m_c_p_tool_0.parameters == 'A{{A:VC/'
    assert f'{type(module_0.MCPTool.from_dict).__module__}.{type(module_0.MCPTool.from_dict).__qualname__}' == 'builtins.method'
    m_c_p_tool_0.to_tool_schema()