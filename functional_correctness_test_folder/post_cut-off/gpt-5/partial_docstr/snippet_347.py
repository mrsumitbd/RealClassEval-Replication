from typing import Dict, Any
from copy import deepcopy


class MessageBuilder:
    @staticmethod
    def build_text_message(content: str) -> Dict[str, Any]:
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        return {
            "msg_type": "text",
            "content": content
        }

    @staticmethod
    def build_markdown_message(content: str, markdown: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        if not isinstance(markdown, dict):
            raise TypeError("markdown must be a dict")
        return {
            "msg_type": "markdown",
            "content": content,
            "markdown": deepcopy(markdown)
        }

    @staticmethod
    def build_image_message(url: str) -> Dict[str, Any]:
        '''构建图片消息'''
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        if not url:
            raise ValueError("url must not be empty")
        return {
            "msg_type": "image",
            "image": {
                "url": url
            }
        }

    @staticmethod
    def build_file_message(file_info: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(file_info, dict):
            raise TypeError("file_info must be a dict")
        if not file_info:
            raise ValueError("file_info must not be empty")
        return {
            "msg_type": "file",
            "file": deepcopy(file_info)
        }

    @staticmethod
    def build_keyboard_message(content: str, keyboard: Dict[str, Any]) -> Dict[str, Any]:
        '''构建带按钮的消息'''
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        if not isinstance(keyboard, dict):
            raise TypeError("keyboard must be a dict")
        return {
            "msg_type": "keyboard",
            "content": content,
            "keyboard": deepcopy(keyboard)
        }

    @staticmethod
    def build_ark_message(ark: Dict[str, Any]) -> Dict[str, Any]:
        '''构建ARK消息'''
        if not isinstance(ark, dict):
            raise TypeError("ark must be a dict")
        if not ark:
            raise ValueError("ark must not be empty")
        return {
            "msg_type": "ark",
            "ark": deepcopy(ark)
        }
