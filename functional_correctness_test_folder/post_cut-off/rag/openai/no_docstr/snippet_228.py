
import os
import tempfile
import shutil
import sys
from typing import Any, Dict, Optional

try:
    import pyperclip
except Exception:
    pyperclip = None

try:
    import clipboard  # third‑party library that supports images on Windows/macOS
except Exception:
    clipboard = None

try:
    from PIL import Image
except Exception:
    Image = None


class ClipboardService:
    """Service for interacting with the system clipboard."""

    def __init__(self):
        """Initialize the clipboard service."""
        self._temp_files = []

    def write_text(self, content: str) -> Dict[str, Any]:
        """
        Write text content to the clipboard.
        Args:
            content: Text content to write to clipboard
        Returns:
            Dict containing success status and any error information
        """
        if pyperclip is None:
            return {"success": False, "error": "pyperclip not available"}
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
        if image is None:
            return None
        try:
            tmp = tempfile.NamedTemporaryFile(
                delete=False, suffix=".png", prefix="clipboard_", dir=None
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
        if pyperclip is None:
            return {"success": False, "error": "pyperclip not available"}
        try:
            text = pyperclip.paste()
            return {"success": True, "content": text, "type": "text"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        """
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        """
        # Try image first (requires clipboard library)
        if clipboard is not None and Image is not None:
            try:
                img = clipboard.paste_image()
                if isinstance(img, Image.Image):
                    tmp_path = self._create_temp_file_from_image(img)
                    if tmp_path:
                        return {
                            "success": True,
                            "type": "image",
                            "file_path": tmp_path,
                        }
            except Exception:
                pass

        # Fallback to text
        result = self.read()
        if result.get("success"):
            result["type"] = "text"
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
