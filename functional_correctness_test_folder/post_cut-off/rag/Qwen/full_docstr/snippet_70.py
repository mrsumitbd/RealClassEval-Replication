
class PrintingCallbackHandler:
    '''Handler for streaming text output and tool invocations to stdout.'''

    def __init__(self) -> None:
        '''Initialize handler.'''
        pass

    def __call__(self, **kwargs: Any) -> None:
        '''Stream text output and tool invocations to stdout.
        Args:
            **kwargs: Callback event data including:
                - reasoningText (Optional[str]): Reasoning text to print if provided.
                - data (str): Text content to stream.
                - complete (bool): Whether this is the final chunk of a response.
                - current_tool_use (dict): Information about the current tool being used.
        '''
        reasoning_text = kwargs.get('reasoningText')
        data = kwargs.get('data', '')
        complete = kwargs.get('complete', False)
        current_tool_use = kwargs.get('current_tool_use', {})

        if reasoning_text:
            print(f"Reasoning: {reasoning_text}")
        if data:
            print(data, end='' if not complete else '\n')
        if current_tool_use:
            print(f"Tool in use: {current_tool_use}")
