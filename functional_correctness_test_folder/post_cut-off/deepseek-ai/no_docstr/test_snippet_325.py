import snippet_325 as module_0

def test_case_0():
    tuple_0 = ()
    agent_info_0 = module_0.AgentInfo(tuple_0, tuple_0)
    assert f'{type(agent_info_0).__module__}.{type(agent_info_0).__qualname__}' == 'snippet_325.AgentInfo'
    assert agent_info_0.name == ()
    assert agent_info_0.description == ()
    assert agent_info_0.file_path is None
    assert agent_info_0.module is None
    assert agent_info_0.yaml_document is None
    assert module_0.TYPE_CHECKING is False
    assert f'{type(module_0.AgentInfo.kind).__module__}.{type(module_0.AgentInfo.kind).__qualname__}' == 'builtins.property'
    assert f'{type(module_0.AgentInfo.path).__module__}.{type(module_0.AgentInfo.path).__qualname__}' == 'builtins.property'