class PrintingCallbackHandler:
    '''Handler for streaming text output and tool invocations to stdout.'''

    def __init__(self) -> None:
        '''Initialize handler.'''
        pass

    def __call__(self, **kwargs: 'Any') -> None:
        '''Stream text output and tool invocations to stdout.
        Args:
            **kwargs: Callback event data including:
                - reasoningText (Optional[str]): Reasoning text to print if provided.
                - data (str): Text content to stream.
                - complete (bool): Whether this is the final chunk of a response.
                - current_tool_use (dict): Information about the current tool being used.
        '''
        import sys

        reasoning_text = kwargs.get("reasoningText")
        if reasoning_text:
            print(f"\n[Reasoning]: {reasoning_text}", file=sys.stdout)

        data = kwargs.get("data")
        if data is not None:
            print(data, end="", flush=True, file=sys.stdout)

        current_tool_use = kwargs.get("current_tool_use")
        if current_tool_use:
            print(f"\n[Tool Use]: {current_tool_use}", file=sys.stdout)

        complete = kwargs.get("complete")
        if complete:
            print("", file=sys.stdout)
