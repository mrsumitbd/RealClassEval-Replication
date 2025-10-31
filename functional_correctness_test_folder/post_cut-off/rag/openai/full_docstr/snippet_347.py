
from typing import Any, Dict


class MessageBuilder:
    '''增强的消息构建器'''

    @staticmethod
    def build_text_message(content: str) -> Dict[str, Any]:
        '''构建文本消息'''
        return {
            'body': content,
        }

    @staticmethod
    def build_markdown_message(content: str, markdown: Dict[str, Any]) -> Dict[str, Any]:
        '''构建Markdown消息'''
        return {
            'body': content,
            'markdown': markdown,
        }

    @staticmethod
    def build_image_message(url: str) -> Dict[str, Any]:
        '''构建图片消息'''
        return {
            'body': '',
            'image_attachment': {
                'url': url,
            },
        }

    @staticmethod
    def build_file_message(file_info: Dict[str, Any]) -> Dict[str, Any]:
        '''构建文件消息'''
        return {
            'body': '',
            'file_attachment': file_info,
        }

    @staticmethod
    def build_keyboard_message(content: str, keyboard: Dict[str, Any]) -> Dict[str, Any]:
        '''构建带按钮的消息'''
        return {
            'body': content,
            'keyboard': keyboard,
        }

    @staticmethod
    def build_ark_message(ark: Dict[str, Any]) -> Dict[str, Any]:
        '''构建ARK消息'''
        return {
            'body': '',
            'ark': ark,
        }
