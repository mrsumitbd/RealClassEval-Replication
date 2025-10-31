from langchain_core.runnables import RunnableConfig, RunnableLambda, Runnable
from typing import Optional, Union, List, Dict, Annotated, Literal, Callable

class Assistant:
    """Represents an assistant that interacts with the LLM."""

    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: Dict, config: RunnableConfig):
        while True:
            current_state = {k: v for k, v in state.items() if k != 'error'}
            result = self.runnable.invoke(current_state)
            empty_response = False
            if not result.tool_calls:
                if not result.content:
                    empty_response = True
                elif isinstance(result.content, list) and (not result.content[0].get('text')):
                    empty_response = True
            if empty_response:
                messages = state['messages'] + [('user', 'Respond with a real output.')]
                state = {**state, 'messages': messages}
            else:
                break
        return {'messages': result}