
from typing import Any, Dict


class MessageBuilder:
    @staticmethod
    def build_text_message(content: str) -> Dict[str, Any]:
        """
        Build a plain text message.

        Parameters
        ----------
        content : str
            The text content of the message.

        Returns
        -------
        Dict[str, Any]
            A dictionary representing the message payload.
        """
        return {
            "type": "text",
            "content": content,
        }

    @staticmethod
    def build_markdown_message(content: str, markdown: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a markdown message.

        Parameters
        ----------
        content : str
            The raw markdown content.
        markdown : Dict[str, Any]
            Parsed markdown metadata (e.g., formatting options).

        Returns
        -------
        Dict[str, Any]
            A dictionary representing the message payload.
        """
        return {
            "type": "markdown",
            "content": content,
            "markdown": markdown,
        }

    @staticmethod
    def build_image_message(url: str) -> Dict[str, Any]:
        """
        Build an image message.

        Parameters
        ----------
        url : str
            The URL of the image.

        Returns
        -------
        Dict[str, Any]
            A dictionary representing the message payload.
        """
        return {
            "type": "image",
            "url": url,
        }

    @staticmethod
    def build_file_message(file_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a file message.

        Parameters
        ----------
        file_info : Dict[str, Any]
            Information about the file (e.g., name, size, url, mime type).

        Returns
        -------
        Dict[str, Any]
            A dictionary representing the message payload.
        """
        return {
            "type": "file",
            "file_info": file_info,
        }

    @staticmethod
    def build_keyboard_message(content: str, keyboard: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a message with an attached keyboard.

        Parameters
        ----------
        content : str
            The text content of the message.
        keyboard : Dict[str, Any]
            Keyboard layout and button definitions.

        Returns
        -------
        Dict[str, Any]
            A dictionary representing the message payload.
        """
        return {
            "type": "keyboard",
            "content": content,
            "keyboard": keyboard,
        }

    @staticmethod
    def build_ark_message(ark: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build an ARK message.

        Parameters
        ----------
        ark : Dict[str, Any]
            ARK-specific payload.

        Returns
        -------
        Dict[str, Any]
            A dictionary representing the message payload.
        """
        return {
            "type": "ark",
            "ark": ark,
        }
