
from typing import Any, Dict


class MessageBuilder:
    '''增强的消息构建器'''

    @staticmethod
    def build_text_message(content: str) -> Dict[str, Any]:
        '''构建文本消息'''
        return {
            'body': content,
            'action_type': 'ma-type:user-generated-message',
        }

    @staticmethod
    def build_markdown_message(content: str, markdown: Dict[str, Any]) -> Dict[str, Any]:
        '''构建Markdown消息'''
        return {
            'body': content,
            'markdown': markdown,
            'action_type': 'ma-type:user-generated-message',
        }

    @staticmethod
    def build_image_message(url: str) -> Dict[str, Any]:
        '''构建图片消息'''
        return {
            'image_attachment': {
                'url': url,
            },
            'action_type': 'ma-type:user-generated-message',
        }

    @staticmethod
    def build_file_message(file_info: Dict[str, Any]) -> Dict[str, Any]:
        '''构建文件消息'''
        return {
            'file_attachment': file_info,
            'action_type': 'ma-type:user-generated-message',
        }

    @staticmethod
    def build_keyboard_message(content: str, keyboard: Dict[str, Any]) -> Dict[str, Any]:
        '''构建带按钮的消息'''
        return {
            'body': content,
            'keyboard': keyboard,
            'action_type': 'ma-type:user-generated-message',
        }

    @staticmethod
    def build_ark_message(ark: Dict[str, Any]) -> Dict[str, Any]:
        '''构建ARK消息'''
        return {
            'ark': ark,
            'action_type': 'ma-type:user-generated-message',
        }
