
class PrintingCallbackHandler:
    '''Handler for streaming text output and tool invocations to stdout.'''

    def __init__(self) -> None:
        '''Initialize handler.'''
        self.current_tool_use = None

    def __call__(self, **kwargs: Any) -> None:
        '''Stream text output and tool invocations to stdout.
        Args:
            **kwargs: Callback event data including:
                - reasoningText (Optional[str]): Reasoning text to print if provided.
                - data (str): Text content to stream.
                - complete (bool): Whether this is the final chunk of a response.
                - current_tool_use (dict): Information about the current tool being used.
        '''
        if 'reasoningText' in kwargs:
            print(f"Reasoning: {kwargs['reasoningText']}")

        if 'data' in kwargs:
            print(kwargs['data'], end='', flush=True)

        if 'complete' in kwargs and kwargs['complete']:
            print()  # New line for completion

        if 'current_tool_use' in kwargs:
            self.current_tool_use = kwargs['current_tool_use']
            print(
                f"\nUsing tool: {self.current_tool_use.get('name', 'unknown')}")
            if 'input' in self.current_tool_use:
                print(f"Tool input: {self.current_tool_use['input']}")
