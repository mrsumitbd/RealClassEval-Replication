from typing import Any

class PrintingCallbackHandler:
    """Handler for streaming text output and tool invocations to stdout."""

    def __init__(self) -> None:
        """Initialize handler."""
        self.tool_count = 0
        self.previous_tool_use = None

    def __call__(self, **kwargs: Any) -> None:
        """Stream text output and tool invocations to stdout.

        Args:
            **kwargs: Callback event data including:
                - reasoningText (Optional[str]): Reasoning text to print if provided.
                - data (str): Text content to stream.
                - complete (bool): Whether this is the final chunk of a response.
                - current_tool_use (dict): Information about the current tool being used.
        """
        reasoningText = kwargs.get('reasoningText', False)
        data = kwargs.get('data', '')
        complete = kwargs.get('complete', False)
        current_tool_use = kwargs.get('current_tool_use', {})
        if reasoningText:
            print(reasoningText, end='')
        if data:
            print(data, end='' if not complete else '\n')
        if current_tool_use and current_tool_use.get('name'):
            tool_name = current_tool_use.get('name', 'Unknown tool')
            if self.previous_tool_use != current_tool_use:
                self.previous_tool_use = current_tool_use
                self.tool_count += 1
                print(f'\nTool #{self.tool_count}: {tool_name}')
        if complete and data:
            print('\n')