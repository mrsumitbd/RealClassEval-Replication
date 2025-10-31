
import os
import tempfile
import shutil
from typing import Dict, Any, Optional, List
from PIL import Image
import sys

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    import tkinter as tk
except ImportError:
    tk = None


class ClipboardService:
    '''Service for interacting with the system clipboard.'''

    def __init__(self):
        '''Initialize the clipboard service.'''
        self._temp_files: List[str] = []

    def write_text(self, content: str) -> Dict[str, Any]:
        '''
        Write content to the clipboard.
        Args:
            content: Content to write to clipboard
        Returns:
            Dict containing success status and any error information
        '''
        try:
            if pyperclip:
                pyperclip.copy(content)
                return {"success": True}
            elif tk:
                root = tk.Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(content)
                root.update()
                root.destroy()
                return {"success": True}
            else:
                return {"success": False, "error": "No clipboard library available"}
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
            fd, path = tempfile.mkstemp(suffix=".png")
            os.close(fd)
            image.save(path, format="PNG")
            self._temp_files.append(path)
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
        try:
            if pyperclip:
                text = pyperclip.paste()
                if text:
                    return {"success": True, "type": "text", "content": text}
            elif tk:
                root = tk.Tk()
                root.withdraw()
                try:
                    text = root.clipboard_get()
                    root.destroy()
                    if text:
                        return {"success": True, "type": "text", "content": text}
                except Exception:
                    root.destroy()
        except Exception as e:
            return {"success": False, "error": str(e)}

        # Try image (only on Windows, using PIL and Tkinter)
        if tk and sys.platform.startswith("win"):
            try:
                root = tk.Tk()
                root.withdraw()
                img = None
                try:
                    root.clipboard_get(type="image")
                except Exception:
                    pass
                try:
                    root.update()
                    img = root.clipboard_get(type="image")
                except Exception:
                    pass
                root.destroy()
                if img:
                    return {"success": True, "type": "image", "content": img}
            except Exception as e:
                return {"success": False, "error": str(e)}

        return {"success": False, "error": "No clipboard content or unsupported type"}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read and process clipboard content, saving images to temp files if needed.
        Returns:
            Dict containing the clipboard content or error information
        '''
        result = self.read()
        if result.get("success") and result.get("type") == "image":
            # Try to convert to PIL Image and save to temp file
            try:
                # This is platform-specific and not always possible
                # For demonstration, we just return the image content
                img = result.get("content")
                if isinstance(img, Image.Image):
                    path = self._create_temp_file_from_image(img)
                    if path:
                        return {"success": True, "type": "image", "file": path}
                    else:
                        return {"success": False, "error": "Failed to save image to temp file"}
                else:
                    return {"success": False, "error": "Clipboard image not a PIL Image"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        return result

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for path in self._temp_files:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
        self._temp_files.clear()

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
