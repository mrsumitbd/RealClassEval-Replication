
from typing import Any, Dict


class MessageBuilder:
    @staticmethod
    def build_text_message(content: str) -> Dict[str, Any]:
        """
        构建文本消息
        """
        return {
            "msg_type": "text",
            "content": {"text": content},
        }

    @staticmethod
    def build_markdown_message(content: str, markdown: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建 Markdown 消息
        """
        return {
            "msg_type": "markdown",
            "content": {
                "content": content,
                "markdown": markdown,
            },
        }

    @staticmethod
    def build_image_message(url: str) -> Dict[str, Any]:
        """
        构建图片消息
        """
        return {
            "msg_type": "image",
            "content": {"url": url},
        }

    @staticmethod
    def build_file_message(file_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建文件消息
        """
        return {
            "msg_type": "file",
            "content": file_info,
        }

    @staticmethod
    def build_keyboard_message(content: str, keyboard: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建带按钮的消息
        """
        return {
            "msg_type": "interactive",
            "content": {
                "content": content,
                "keyboard": keyboard,
            },
        }

    @staticmethod
    def build_ark_message(ark: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建 ARK 消息
        """
        return {
            "msg_type": "ark",
            "content": ark,
        }
