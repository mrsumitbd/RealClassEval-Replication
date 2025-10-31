
import os
import tempfile
import shutil
from typing import Dict, Any, Optional, List
import pyperclip
from PIL import Image, ImageGrab


class ClipboardService:
    """Service for interacting with the system clipboard."""

    def __init__(self):
        """Initialize the clipboard service."""
        # Keep track of temporary files created for images or binary data
        self._temp_files: List[str] = []

    def write_text(self, content: str) -> Dict[str, Any]:
        """
        Write text content to the clipboard.
        Args:
            content: Text content to write to clipboard
        Returns:
            Dict containing success status and any error information
        """
        try:
            pyperclip.copy(content)
            return {"success": True}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def _create_temp_file_from_image(self, image: Image.Image) -> Optional[str]:
        """
        Create a temporary file from a PIL Image.
        Args:
            image: PIL Image object
        Returns:
            Path to the temporary file or None if failed
        """
        try:
            tmp = tempfile.NamedTemporaryFile(
                delete=False, suffix=".png", prefix="clipboard_", mode="wb"
            )
            image.save(tmp, format="PNG")
            tmp_path = tmp.name
            tmp.close()
            self._temp_files.append(tmp_path)
            return tmp_path
        except Exception:
            return None

    def read(self) -> Dict[str, Any]:
        """
        Read content from the clipboard and automatically determine the content type.
        Returns:
            Dict containing the clipboard content or error information
        """
        # Try to grab an image or file list first
        try:
            clip = ImageGrab.grabclipboard()
            if isinstance(clip, Image.Image):
                # Image
                tmp_path = self._create_temp_file_from_image(clip)
                if tmp_path:
                    return {"type": "image", "path": tmp_path}
                else:
                    return {"type": "image", "error": "Failed to create temp file"}
            if isinstance(clip, list):
                # List of file paths (e.g., dragged files)
                return {"type": "file", "paths": clip}
        except Exception:
            # ignore and fall back to text
            pass

        # Fallback to text
        try:
            text = pyperclip.paste()
            return {"type": "text", "content": text}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        """
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        """
        result = self.read()
        if result.get("type") == "image" and "path" in result:
            # Return a command that can be used to open the image file
            return {"command": "open_file", "path": result["path"]}
        if result.get("type") == "file" and "paths" in result:
            # Return the first file path for simplicity
            return {"command": "open_file", "path": result["paths"][0]}
        if result.get("type") == "text":
            return {"type": "text", "content": result["content"]}
        # If we got an error
        return result

    def cleanup_temp_files(self):
        """Clean up any temporary files created by this service."""
        for path in self._temp_files:
            try:
                os.remove(path)
            except Exception:
                pass
        self._temp_files.clear()

    def __del__(self):
        """Cleanup temporary files when the service is destroyed."""
        self.cleanup_temp_files()
