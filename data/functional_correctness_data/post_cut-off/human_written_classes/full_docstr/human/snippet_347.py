from typing import Dict, Any, Optional, Union

class MessageBuilder:
    """增强的消息构建器"""

    @staticmethod
    def build_text_message(content: str) -> Dict[str, Any]:
        """构建文本消息"""
        return {'content': content, 'msg_type': MessageType.TEXT.value}

    @staticmethod
    def build_markdown_message(content: str, markdown: Dict[str, Any]) -> Dict[str, Any]:
        """构建Markdown消息"""
        return {'content': content, 'msg_type': MessageType.MARKDOWN.value, 'markdown': markdown}

    @staticmethod
    def build_image_message(url: str) -> Dict[str, Any]:
        """构建图片消息"""
        return {'msg_type': MessageType.IMAGE.value, 'image': url}

    @staticmethod
    def build_file_message(file_info: Dict[str, Any]) -> Dict[str, Any]:
        """构建文件消息"""
        return {'msg_type': MessageType.FILE.value, 'media': file_info}

    @staticmethod
    def build_keyboard_message(content: str, keyboard: Dict[str, Any]) -> Dict[str, Any]:
        """构建带按钮的消息"""
        return {'content': content, 'msg_type': MessageType.TEXT.value, 'keyboard': keyboard}

    @staticmethod
    def build_ark_message(ark: Dict[str, Any]) -> Dict[str, Any]:
        """构建ARK消息"""
        return {'msg_type': MessageType.ARK.value, 'ark': ark}