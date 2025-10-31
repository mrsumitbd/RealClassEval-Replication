
from typing import Dict, Any


class MessageBuilder:

    @staticmethod
    def build_text_message(content: str) -> Dict[str, Any]:
        return {
            "type": "text",
            "content": content
        }

    @staticmethod
    def build_markdown_message(content: str, markdown: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "markdown",
            "content": content,
            "markdown": markdown
        }

    @staticmethod
    def build_image_message(url: str) -> Dict[str, Any]:
        '''构建图片消息'''
        return {
            "type": "image",
            "url": url
        }

    @staticmethod
    def build_file_message(file_info: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "file",
            "file": file_info
        }

    @staticmethod
    def build_keyboard_message(content: str, keyboard: Dict[str, Any]) -> Dict[str, Any]:
        '''构建带按钮的消息'''
        return {
            "type": "keyboard",
            "content": content,
            "keyboard": keyboard
        }

    @staticmethod
    def build_ark_message(ark: Dict[str, Any]) -> Dict[str, Any]:
        '''构建ARK消息'''
        return {
            "type": "ark",
            "ark": ark
        }
