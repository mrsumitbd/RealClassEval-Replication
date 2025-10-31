from minitap.mobile_use.sdk.builders.task_request_builder import TaskRequestCommonBuilder
from minitap.mobile_use.sdk.builders.agent_config_builder import AgentConfigBuilder

class BuildersWrapper:

    @property
    def AgentConfig(self) -> AgentConfigBuilder:
        return AgentConfigBuilder()

    @property
    def TaskDefaults(self) -> TaskRequestCommonBuilder:
        return TaskRequestCommonBuilder()