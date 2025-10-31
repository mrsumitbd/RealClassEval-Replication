import pytest
import snippet_213 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = "T'a*"
    local_bedrock_agent_core_client_0 = module_0.LocalBedrockAgentCoreClient(str_0)
    local_bedrock_agent_core_client_0.invoke_endpoint(str_0, str_0, local_bedrock_agent_core_client_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = 't\x0cx-'
    local_bedrock_agent_core_client_0 = module_0.LocalBedrockAgentCoreClient(str_0)
    none_type_0 = None
    local_bedrock_agent_core_client_0.invoke_endpoint(local_bedrock_agent_core_client_0, none_type_0, none_type_0)

def test_case_2():
    str_0 = ''
    module_0.LocalBedrockAgentCoreClient(str_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = '`UaN],3:G9'
    local_bedrock_agent_core_client_0 = module_0.LocalBedrockAgentCoreClient(str_0)
    local_bedrock_agent_core_client_1 = module_0.LocalBedrockAgentCoreClient(str_0)
    str_1 = 'Ex]Z;s4)jW*zlD3'
    none_type_0 = None
    local_bedrock_agent_core_client_0.invoke_endpoint(none_type_0, local_bedrock_agent_core_client_1, str_1)