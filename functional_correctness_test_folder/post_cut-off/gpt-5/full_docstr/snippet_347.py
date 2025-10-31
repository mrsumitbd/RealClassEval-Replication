from typing import Any, Dict


class MessageBuilder:
    '''增强的消息构建器'''

    @staticmethod
    def _ensure_str(name: str, value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError(f'{name} must be a string')
        v = value.strip()
        if not v:
            raise ValueError(f'{name} cannot be empty')
        return v

    @staticmethod
    def _ensure_dict(name: str, value: Any) -> Dict[str, Any]:
        if not isinstance(value, dict):
            raise TypeError(f'{name} must be a dict')
        return dict(value)

    @staticmethod
    def build_text_message(content: str) -> Dict[str, Any]:
        '''构建文本消息'''
        text = MessageBuilder._ensure_str('content', content)
        return {
            'msg_type': 'text',
            'content': text,
        }

    @staticmethod
    def build_markdown_message(content: str, markdown: Dict[str, Any]) -> Dict[str, Any]:
        '''构建Markdown消息'''
        text = MessageBuilder._ensure_str('content', content)
        md = MessageBuilder._ensure_dict('markdown', markdown)
        return {
            'msg_type': 'markdown',
            'content': text,
            'markdown': md,
        }

    @staticmethod
    def build_image_message(url: str) -> Dict[str, Any]:
        '''构建图片消息'''
        image_url = MessageBuilder._ensure_str('url', url)
        return {
            'msg_type': 'image',
            'image': {
                'url': image_url,
            },
        }

    @staticmethod
    def build_file_message(file_info: Dict[str, Any]) -> Dict[str, Any]:
        '''构建文件消息'''
        info = MessageBuilder._ensure_dict('file_info', file_info)
        if not info:
            raise ValueError('file_info cannot be empty')
        return {
            'msg_type': 'file',
            'file': info,
        }

    @staticmethod
    def build_keyboard_message(content: str, keyboard: Dict[str, Any]) -> Dict[str, Any]:
        '''构建带按钮的消息'''
        text = MessageBuilder._ensure_str('content', content)
        kb = MessageBuilder._ensure_dict('keyboard', keyboard)
        if not kb:
            raise ValueError('keyboard cannot be empty')
        return {
            'msg_type': 'keyboard',
            'content': text,
            'keyboard': kb,
        }

    @staticmethod
    def build_ark_message(ark: Dict[str, Any]) -> Dict[str, Any]:
        '''构建ARK消息'''
        ark_payload = MessageBuilder._ensure_dict('ark', ark)
        if not ark_payload:
            raise ValueError('ark cannot be empty')
        return {
            'msg_type': 'ark',
            'ark': ark_payload,
        }
