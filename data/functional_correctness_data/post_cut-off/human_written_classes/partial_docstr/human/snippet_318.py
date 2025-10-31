from copy import deepcopy
from loguru import logger
from tau2.utils.llm_utils import generate
from tau2.data_model.message import AssistantMessage, Message, SystemMessage, UserMessage
from tau2.environment.environment import Environment
from typing import Callable, Optional
from tau2.config import DEFAULT_LLM_ENV_INTERFACE, DEFAULT_LLM_ENV_INTERFACE_ARGS

class InterfaceAgent:

    def __init__(self, environment: Environment, llm: Optional[str]=DEFAULT_LLM_ENV_INTERFACE, llm_args: Optional[dict]=DEFAULT_LLM_ENV_INTERFACE_ARGS):
        """
        Initialize the InterfaceAgent.
        """
        self.messages = []
        self.environment = environment
        self.llm = llm
        self.llm_args = deepcopy(llm_args) if llm_args is not None else {}

    @property
    def system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def respond(self, message: str, message_history: Optional[list[Message]]=None) -> tuple[AssistantMessage, list[Message]]:
        """
        Respond to a user message.
        """
        if message_history is None:
            message_history = []
        system_message = SystemMessage(role='system', content=self.system_prompt)
        user_message = UserMessage(role='user', content=message)
        message_history.append(user_message)
        messages = [system_message] + message_history
        assistant_message = generate(model=self.llm, tools=self.environment.get_tools(), messages=messages, **self.llm_args)
        while assistant_message.is_tool_call():
            message_history.append(assistant_message)
            for tool_call in assistant_message.tool_calls:
                tool_message = self.environment.get_response(tool_call)
                message_history.append(tool_message)
            messages = [system_message] + message_history
            assistant_message = generate(model=self.llm, tools=self.environment.get_tools(), messages=messages, **self.llm_args)
        message_history.append(assistant_message)
        return (assistant_message, message_history)

    def set_seed(self, seed: int):
        """Set the seed for the LLM."""
        if self.llm is None:
            raise ValueError('LLM is not set')
        cur_seed = self.llm_args.get('seed', None)
        if cur_seed is not None:
            logger.warning(f'Seed is already set to {cur_seed}, resetting it to {seed}')
        self.llm_args['seed'] = seed