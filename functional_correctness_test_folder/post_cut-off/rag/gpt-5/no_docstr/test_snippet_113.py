import pytest
import snippet_113 as module_0

def test_case_0():
    biomni_config_0 = module_0.BiomniConfig()
    assert f'{type(biomni_config_0).__module__}.{type(biomni_config_0).__qualname__}' == 'snippet_113.BiomniConfig'
    assert biomni_config_0.path == './data'
    assert biomni_config_0.timeout_seconds == 600
    assert biomni_config_0.llm == 'claude-sonnet-4-20250514'
    assert biomni_config_0.temperature == pytest.approx(0.7, abs=0.01, rel=0.01)
    assert biomni_config_0.use_tool_retriever is True
    assert biomni_config_0.base_url is None
    assert biomni_config_0.api_key is None
    assert biomni_config_0.source is None
    assert module_0.BiomniConfig.path == './data'
    assert module_0.BiomniConfig.timeout_seconds == 600
    assert module_0.BiomniConfig.llm == 'claude-sonnet-4-20250514'
    assert module_0.BiomniConfig.temperature == pytest.approx(0.7, abs=0.01, rel=0.01)
    assert module_0.BiomniConfig.use_tool_retriever is True
    assert module_0.BiomniConfig.base_url is None
    assert module_0.BiomniConfig.api_key is None
    assert module_0.BiomniConfig.source is None

def test_case_1():
    none_type_0 = None
    biomni_config_0 = module_0.BiomniConfig(base_url=none_type_0)
    assert f'{type(biomni_config_0).__module__}.{type(biomni_config_0).__qualname__}' == 'snippet_113.BiomniConfig'
    assert biomni_config_0.path == './data'
    assert biomni_config_0.timeout_seconds == 600
    assert biomni_config_0.llm == 'claude-sonnet-4-20250514'
    assert biomni_config_0.temperature == pytest.approx(0.7, abs=0.01, rel=0.01)
    assert biomni_config_0.use_tool_retriever is True
    assert biomni_config_0.base_url is None
    assert biomni_config_0.api_key is None
    assert biomni_config_0.source is None
    assert module_0.BiomniConfig.path == './data'
    assert module_0.BiomniConfig.timeout_seconds == 600
    assert module_0.BiomniConfig.llm == 'claude-sonnet-4-20250514'
    assert module_0.BiomniConfig.temperature == pytest.approx(0.7, abs=0.01, rel=0.01)
    assert module_0.BiomniConfig.use_tool_retriever is True
    assert module_0.BiomniConfig.base_url is None
    assert module_0.BiomniConfig.api_key is None
    assert module_0.BiomniConfig.source is None
    biomni_config_0.to_dict()