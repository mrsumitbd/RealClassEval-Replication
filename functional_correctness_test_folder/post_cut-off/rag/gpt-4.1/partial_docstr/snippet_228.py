
import os
import tempfile
import shutil
from typing import Dict, Any, Optional
from PIL import Image
import sys

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None


class ClipboardService:
    '''Service for interacting with the system clipboard.'''

    def __init__(self):
        '''Initialize the clipboard service.'''
        self._temp_files = set()
        self._temp_dir = tempfile.mkdtemp(prefix="clipboard_service_")

    def write_text(self, content: str) -> Dict[str, Any]:
        '''
        Write text content to the clipboard.
        Args:
            content: Text content to write to clipboard
        Returns:
            Dict containing success status and any error information
        '''
        if not pyperclip:
            return {"success": False, "error": "pyperclip not installed"}
        try:
            pyperclip.copy(content)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _create_temp_file_from_image(self, image: Image.Image) -> Optional[str]:
        '''
        Create a temporary file from a PIL Image.
        Args:
            image: PIL Image object
        Returns:
            Path to the temporary file or None if failed
        '''
        try:
            fd, path = tempfile.mkstemp(suffix=".png", dir=self._temp_dir)
            os.close(fd)
            image.save(path, format="PNG")
            self._temp_files.add(path)
            return path
        except Exception:
            return None

    def read(self) -> Dict[str, Any]:
        '''
        Read content from the clipboard and automatically determine the content type.
        Returns:
            Dict containing the clipboard content or error information
        '''
        # Try text first
        if not pyperclip:
            return {"success": False, "error": "pyperclip not installed"}
        try:
            text = pyperclip.paste()
            if text:
                return {"success": True, "type": "text", "content": text}
        except Exception as e:
            return {"success": False, "error": str(e)}

        # Try image (platform dependent)
        if ImageGrab:
            try:
                img = ImageGrab.grabclipboard()
                if isinstance(img, Image.Image):
                    return {"success": True, "type": "image", "content": img}
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "No clipboard content or unsupported type"}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        result = self.read()
        if not result.get("success"):
            return result

        if result.get("type") == "text":
            return {"success": True, "type": "text", "content": result["content"]}
        elif result.get("type") == "image":
            img = result["content"]
            path = self._create_temp_file_from_image(img)
            if path:
                return {
                    "success": True,
                    "type": "file",
                    "file_path": path,
                    "file_command": f"file://{path}"
                }
            else:
                return {"success": False, "error": "Failed to create temp file from image"}
        else:
            return {"success": False, "error": "Unsupported clipboard content type"}

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for path in list(self._temp_files):
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
            self._temp_files.discard(path)
        try:
            if os.path.exists(self._temp_dir) and not os.listdir(self._temp_dir):
                shutil.rmtree(self._temp_dir)
        except Exception:
            pass

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
