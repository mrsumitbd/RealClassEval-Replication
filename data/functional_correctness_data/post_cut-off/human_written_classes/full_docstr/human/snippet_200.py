import re
from viby.llm.client import create_openai_client
from viby.config import config
from typing import Dict, Any, List, Tuple
from viby.locale import get_text

class CompactionManager:
    """
    消息压缩管理器 - 提供智能消息历史压缩功能
    实现了智能压缩算法，使得在保持语义和关键信息的同时减少token数量
    """
    _chinese_pattern = re.compile('[\\u4e00-\\u9fff]')
    CHINESE_DIVIDER = 1.5
    NON_CHINESE_DIVIDER = 4
    PADDING = 3
    MESSAGE_OVERHEAD = 4
    FORMATTING_OVERHEAD = 3

    def __init__(self):
        """初始化压缩管理器"""
        self.config = config
        self.autocompact_config = self.config.autocompact
        self.compaction_stats = {'total_compressions': 0, 'tokens_before_compression': 0, 'tokens_after_compression': 0, 'compression_ratio': 0.0}

    def _estimate_token_count(self, text: str) -> int:
        """
        简单估算文本的token数量 - 不使用tokenizer

        Args:
            text: 需要估算token数的文本

        Returns:
            估算的token数量
        """
        if not text:
            return 0
        chinese_chars = len(self._chinese_pattern.findall(text))
        non_chinese_chars = len(text) - chinese_chars
        tokens = chinese_chars / self.CHINESE_DIVIDER + non_chinese_chars / self.NON_CHINESE_DIVIDER
        return int(tokens) + self.PADDING

    def _count_tokens_in_messages(self, messages: List[Dict[str, Any]]) -> int:
        """
        计算消息列表中的总token数

        Args:
            messages: 消息列表

        Returns:
            总token数
        """
        base = sum((self._estimate_token_count(m.get('content', '')) + self.MESSAGE_OVERHEAD for m in messages))
        return int(base + self.FORMATTING_OVERHEAD)

    def should_compact(self, messages: List[Dict[str, Any]], model_config: Dict[str, Any]) -> bool:
        """
        根据token数量判断是否应该压缩消息历史

        Args:
            messages: 消息历史
            model_config: 模型配置

        Returns:
            是否应该压缩
        """
        if not self.autocompact_config.enabled:
            return False
        if not any((m.get('role') == 'user' for m in messages)) or not any((m.get('role') == 'assistant' for m in messages)):
            return False
        max_tokens = model_config.get('max_tokens', 8192)
        return self._count_tokens_in_messages(messages) > int(max_tokens * self.autocompact_config.threshold_ratio)

    def _format_conversation_for_compression(self, messages: List[Dict[str, Any]]) -> str:
        """
        将消息列表格式化为适合压缩的文本格式

        Args:
            messages: 消息列表

        Returns:
            格式化后的对话文本
        """
        result = []
        for message in messages:
            role = message.get('role', '').upper()
            content = message.get('content', '')
            result.append(f'{role}: {content}')
        return '\n\n'.join(result)

    def _expand_compressed_to_messages(self, compressed_text: str, original_messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        将压缩后的文本扩展为消息列表

        Args:
            compressed_text: 压缩后的对话摘要文本
            original_messages: 原始消息列表

        Returns:
            包含压缩摘要的消息列表
        """
        system_messages = [m for m in original_messages if m.get('role') == 'system']
        tool_messages = [m for m in original_messages if m.get('role') == 'tool']
        compressed_summary = {'role': 'assistant', 'content': get_text('HISTORY', 'compressed_summary_prefix') + compressed_text}
        return system_messages + tool_messages + [compressed_summary]

    def compact_messages(self, messages: List[Dict[str, Any]], model_config: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """压缩消息历史，保留关键信息并减少 token 数量。"""
        if not any((m.get('role') in ('user', 'assistant') for m in messages)):
            return (messages, {'compressed': False, 'reason': 'no_conversation_messages'})
        if not self.should_compact(messages, model_config):
            return (messages, {'compressed': False, 'reason': 'below_threshold'})
        try:
            keep_exchanges = self.autocompact_config.keep_last_exchanges
            kept_msgs = []
            user_assistant_pairs = 0
            temp_msgs = list(reversed(messages))
            for msg in temp_msgs:
                role = msg.get('role')
                if role in ('user', 'assistant'):
                    kept_msgs.append(msg)
                    if len(kept_msgs) >= 2 and kept_msgs[-1].get('role') != kept_msgs[-2].get('role'):
                        user_assistant_pairs += 1
                        if user_assistant_pairs >= keep_exchanges:
                            break
            kept_msgs = list(reversed(kept_msgs))
            msgs_to_compress = []
            for msg in messages:
                if msg.get('role') in ('user', 'assistant') and msg not in kept_msgs:
                    msgs_to_compress.append(msg)
            if len(msgs_to_compress) < 1:
                return (messages, {'compressed': False, 'reason': 'too_few_messages_to_compress'})
            conversation_text = self._format_conversation_for_compression(msgs_to_compress)
            fast_model_config = self.config.get_model_config('fast')
            if not fast_model_config.get('model'):
                fast_model_config = model_config
            client = create_openai_client(fast_model_config.get('api_key', ''), fast_model_config.get('base_url', ''))
            response = client.chat.completions.create(model=fast_model_config.get('model'), messages=[{'role': 'system', 'content': get_text('HISTORY', 'compaction_system_prompt')}, {'role': 'user', 'content': get_text('HISTORY', 'compaction_user_prompt').format(conversation_text)}], temperature=0.3)
            compressed_text = response.choices[0].message.content
        except Exception as e:
            logger.error(f'压缩过程出错: {e}')
            return (messages, {'compressed': False, 'reason': f'error: {str(e)}'})
        compressed_messages = self._expand_compressed_to_messages(compressed_text, messages) + kept_msgs
        tokens_before = self._count_tokens_in_messages(messages)
        tokens_after = self._count_tokens_in_messages(compressed_messages)
        self.compaction_stats = {'total_compressions': self.compaction_stats['total_compressions'] + 1, 'tokens_before_compression': tokens_before, 'tokens_after_compression': tokens_after, 'tokens_saved': tokens_before - tokens_after, 'compression_ratio': tokens_after / tokens_before if tokens_before else 1.0}
        compression_stats = {'compressed': True, 'tokens_before': tokens_before, 'tokens_after': tokens_after, 'tokens_saved': tokens_before - tokens_after, 'compression_ratio': self.compaction_stats['compression_ratio'], 'kept_exchanges': len(kept_msgs) // 2}
        logger.info(f"对话压缩完成: {tokens_before} -> {tokens_after} tokens (压缩率: {compression_stats['compression_ratio']:.2f})")
        return (compressed_messages, compression_stats)