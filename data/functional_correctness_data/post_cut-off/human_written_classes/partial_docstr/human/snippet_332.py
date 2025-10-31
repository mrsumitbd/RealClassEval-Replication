import tiktoken
from typing import List, Dict, Any

class TokenCounter:
    _accumulated_tokens = {'input': 0, 'output': 0}
    _accumulated_cost = {'input': 0.0, 'output': 0.0, 'tool_cost': 0.0}

    def __init__(self):
        self.model_name = get_model_name()

    @classmethod
    def get_accumulated_stats(cls) -> Dict[str, Dict[str, float]]:
        """Get accumulated token usage and costs across all instances."""
        return {'tokens': dict(cls._accumulated_tokens), 'costs': dict(cls._accumulated_cost), 'total_cost': sum(cls._accumulated_cost.values())}

    def count_output_tokens(self, string: str) -> int:
        """
        MetaGPT anthropic client token counter does not work for anthropic>=0.39.0: https://github.com/geekan/MetaGPT/blob/main/metagpt/utils/token_counter.py#L479C1-L480C1
        Use simple tokenizer instead, since that is what langchain_aws is doing: 
            - https://github.com/langchain-ai/langchain-aws/commit/6355b0ff44c92b594ab8c3a5c50ac726904d716d
            - https://github.com/langchain-ai/langchain-aws/issues/314
            - https://python.langchain.com/api_reference/_modules/langchain_core/language_models/base.html#BaseLanguageModel

        Returns the number of tokens in a text string.

        Args:
            string (str): The text string.

        Returns:
            int: The number of tokens in the text string.
        """
        try:
            encoding = tiktoken.encoding_for_model(self.model_name)
        except KeyError:
            bench_logger.debug(f'Warning: model {self.model_name} not found in tiktoken. Using cl100k_base encoding.')
            encoding = tiktoken.get_encoding('cl100k_base')
        try:
            token_count = len(encoding.encode(string))
            return token_count
        except Exception as e:
            bench_logger.error(f'Error in token counting: {e}')
            return 0