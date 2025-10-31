class HandoffAgentWrapper:

    def __init__(self, agent):
        self.agent = agent

    def get_agent(self):
        return self.agent