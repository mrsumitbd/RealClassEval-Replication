
from typing import Dict, Any


class MessageBuilder:

    @staticmethod
    def build_text_message(content: str) -> Dict[str, Any]:
        return {
            "content": content
        }

    @staticmethod
    def build_markdown_message(content: str, markdown: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "content": content,
            "markdown": markdown
        }

    @staticmethod
    def build_image_message(url: str) -> Dict[str, Any]:
        return {
            "image": url
        }

    @staticmethod
    def build_file_message(file_info: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "file": file_info
        }

    @staticmethod
    def build_keyboard_message(content: str, keyboard: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "content": content,
            "keyboard": keyboard
        }

    @staticmethod
    def build_ark_message(ark: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "ark": ark
        }
