class ToolBasedAuthorizer:
    """
    Work In Progress: Implement tool based white-listing
    of what jobs can run and what those jobs can do.
    """

    def __init__(self, toolbox):
        self.toolbox = toolbox

    def get_authorization(self, tool_id):
        tool = None
        try:
            tool = self.toolbox.get_tool(tool_id)
        except Exception:
            pass
        return ToolBasedAuthorization(tool)