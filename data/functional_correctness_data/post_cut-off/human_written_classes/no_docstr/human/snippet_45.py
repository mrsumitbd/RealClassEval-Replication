from ii_agent.utils.constants import WorkSpaceMode

class SystemPromptBuilder:

    def __init__(self, workspace_mode: WorkSpaceMode, sequential_thinking: bool):
        self.workspace_mode = workspace_mode
        self.default_system_prompt = get_system_prompt(workspace_mode) if not sequential_thinking else get_system_prompt_with_seq_thinking(workspace_mode)
        self.system_prompt = self.default_system_prompt

    def reset_system_prompt(self):
        self.system_prompt = self.default_system_prompt

    def get_system_prompt(self):
        return self.system_prompt

    def update_web_dev_rules(self, web_dev_rules: str):
        self.system_prompt = f'{self.default_system_prompt}\n<web_framework_rules>\n{web_dev_rules}\n</web_framework_rules>\n'