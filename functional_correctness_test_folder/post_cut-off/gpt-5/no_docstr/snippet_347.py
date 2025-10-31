from typing import Dict, Any
import copy


class MessageBuilder:
    @staticmethod
    def _ensure_str_nonempty(value: str, name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        value_stripped = value.strip()
        if not value_stripped:
            raise ValueError(f"{name} must be a non-empty string")
        return value_stripped

    @staticmethod
    def _ensure_dict(value: Dict[str, Any], name: str) -> Dict[str, Any]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a dict")
        if not value:
            raise ValueError(f"{name} must not be empty")
        return value

    @staticmethod
    def build_text_message(content: str) -> Dict[str, Any]:
        content = MessageBuilder._ensure_str_nonempty(content, "content")
        return {"type": "text", "data": {"content": content}}

    @staticmethod
    def build_markdown_message(content: str, markdown: Dict[str, Any]) -> Dict[str, Any]:
        content = MessageBuilder._ensure_str_nonempty(content, "content")
        markdown = MessageBuilder._ensure_dict(markdown, "markdown")
        return {"type": "markdown", "data": {"content": content, "markdown": copy.deepcopy(markdown)}}

    @staticmethod
    def build_image_message(url: str) -> Dict[str, Any]:
        url = MessageBuilder._ensure_str_nonempty(url, "url")
        if not (url.startswith("http://") or url.startswith("https://")):
            raise ValueError("url must start with http:// or https://")
        return {"type": "image", "data": {"url": url}}

    @staticmethod
    def build_file_message(file_info: Dict[str, Any]) -> Dict[str, Any]:
        file_info = MessageBuilder._ensure_dict(file_info, "file_info")
        return {"type": "file", "data": copy.deepcopy(file_info)}

    @staticmethod
    def build_keyboard_message(content: str, keyboard: Dict[str, Any]) -> Dict[str, Any]:
        content = MessageBuilder._ensure_str_nonempty(content, "content")
        keyboard = MessageBuilder._ensure_dict(keyboard, "keyboard")
        return {"type": "keyboard", "data": {"content": content, "keyboard": copy.deepcopy(keyboard)}}

    @staticmethod
    def build_ark_message(ark: Dict[str, Any]) -> Dict[str, Any]:
        ark = MessageBuilder._ensure_dict(ark, "ark")
        return {"type": "ark", "data": copy.deepcopy(ark)}
