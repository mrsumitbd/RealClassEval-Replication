
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
        # Try to grab image or file list first (Windows/macOS)
        try:
            clip = ImageGrab.grabclipboard()
            if isinstance(clip, Image.Image):
                return {"type": "image", "data": clip}
            if isinstance(clip, list) and clip:
                # Assume list of file paths
                return {"type": "file", "path": clip[0]}
        except Exception:
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
        if not result.get("type"):
            return result  # error case

        if result["type"] == "image":
            tmp_path = self._create_temp_file_from_image(result["data"])
            if tmp_path:
                return {"type": "file", "path": tmp_path}
            else:
                return {"success": False, "error": "Failed to create temp file from image"}
        if result["type"] == "file":
            # Already a file path; just return it
            return {"type": "file", "path": result["path"]}

        # Text case
        return {"type": "text", "content": result["content"]}

    def cleanup_temp_files(self):
        """Clean up any temporary files created by this service."""
        for path in self._temp_files:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
        self._temp_files.clear()

    def __del__(self):
        """Cleanup temporary files when the service is destroyed."""
        self.cleanup_temp_files()
