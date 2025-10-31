from typing import Dict, Any
import copy


class MessageBuilder:
    '''增强的消息构建器'''

    @staticmethod
    def build_text_message(content: str) -> Dict[str, Any]:
        '''构建文本消息'''
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        return {"content": content}

    @staticmethod
    def build_markdown_message(content: str, markdown: Dict[str, Any]) -> Dict[str, Any]:
        '''构建Markdown消息'''
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        if not isinstance(markdown, dict):
            raise TypeError("markdown must be a dict")
        return {"content": content, "markdown": copy.deepcopy(markdown)}

    @staticmethod
    def build_image_message(url: str) -> Dict[str, Any]:
        '''构建图片消息'''
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        return {"image": url}

    @staticmethod
    def build_file_message(file_info: Dict[str, Any]) -> Dict[str, Any]:
        '''构建文件消息'''
        if not isinstance(file_info, dict):
            raise TypeError("file_info must be a dict")
        return {"file_info": copy.deepcopy(file_info)}

    @staticmethod
    def build_keyboard_message(content: str, keyboard: Dict[str, Any]) -> Dict[str, Any]:
        '''构建带按钮的消息'''
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        if not isinstance(keyboard, dict):
            raise TypeError("keyboard must be a dict")
        return {"content": content, "keyboard": copy.deepcopy(keyboard)}

    @staticmethod
    def build_ark_message(ark: Dict[str, Any]) -> Dict[str, Any]:
        '''构建ARK消息'''
        if not isinstance(ark, dict):
            raise TypeError("ark must be a dict")
        return {"ark": copy.deepcopy(ark)}
