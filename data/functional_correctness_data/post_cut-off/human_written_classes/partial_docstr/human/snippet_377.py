from typing import Dict, Any, List, Optional, Tuple
from viby.locale import get_text
import time

class TokenTracker:
    """记录和跟踪LLM API调用的token使用情况"""

    def __init__(self):
        self.reset()
        self.model_name = None

    def reset(self):
        """重置所有计数器"""
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self.start_time = time.time()
        self.end_time = None

    def update_counters(self, usage):
        """从响应中更新token计数"""
        try:
            if not usage:
                return False
            if hasattr(usage, 'prompt_tokens'):
                self.prompt_tokens = usage.prompt_tokens
            if hasattr(usage, 'completion_tokens'):
                self.completion_tokens = usage.completion_tokens
            if hasattr(usage, 'total_tokens'):
                self.total_tokens = usage.total_tokens
            else:
                self.total_tokens = self.prompt_tokens + self.completion_tokens
            return True
        except (AttributeError, TypeError):
            return False

    def update_from_response(self, response):
        """从完整响应中更新token计数"""
        usage = getattr(response, 'usage', None)
        return self.update_counters(usage)

    def update_from_chunk(self, chunk):
        """从流式响应块中更新token计数"""
        usage = getattr(chunk, 'usage', None)
        return self.update_counters(usage)

    def get_formatted_stats(self) -> List[str]:
        """获取格式化的统计信息行"""
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        stats = []
        stats.append(get_text('GENERAL', 'token_usage_title'))
        stats.append(get_text('GENERAL', 'token_usage_prompt').format(self.prompt_tokens))
        stats.append(get_text('GENERAL', 'token_usage_completion').format(self.completion_tokens))
        stats.append(get_text('GENERAL', 'token_usage_total').format(self.total_tokens))
        stats.append(get_text('GENERAL', 'token_usage_duration').format(f'{duration:.2f}s'))
        return stats