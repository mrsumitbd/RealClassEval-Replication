
import os
import tempfile
import shutil
from typing import Dict, Any, Optional
from PIL import Image
import io
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
    import tkinter as tk
except ImportError:
    tk = None

try:
    import win32clipboard
    import win32con
except ImportError:
    win32clipboard = None


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
        try:
            if pyperclip:
                text = pyperclip.paste()
                if text:
                    return {"type": "text", "content": text}
            elif tk:
                root = tk.Tk()
                root.withdraw()
                text = root.clipboard_get()
                root.destroy()
                if text:
                    return {"type": "text", "content": text}
        except Exception:
            pass

        # Try image (Windows only)
        if win32clipboard:
            try:
                win32clipboard.OpenClipboard()
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB):
                    data = win32clipboard.GetClipboardData(win32con.CF_DIB)
                    if data:
                        # Convert DIB to PIL Image
                        import PIL.Image
                        import PIL.ImageGrab
                        image = PIL.ImageGrab.grabclipboard()
                        if isinstance(image, Image.Image):
                            win32clipboard.CloseClipboard()
                            return {"type": "image", "content": image}
                win32clipboard.CloseClipboard()
            except Exception:
                try:
                    win32clipboard.CloseClipboard()
                except Exception:
                    pass

        # Try image (Linux/Mac)
        try:
            from PIL import ImageGrab
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image):
                return {"type": "image", "content": image}
        except Exception:
            pass

        return {"type": "unknown", "error": "No clipboard content or unsupported type"}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        result = self.read()
        if result.get("type") == "image" and isinstance(result.get("content"), Image.Image):
            image = result["content"]
            path = self._create_temp_file_from_image(image)
            if path:
                return {"type": "file", "file_path": path, "command": f"file:{path}"}
            else:
                return {"type": "error", "error": "Failed to create temp file from image"}
        elif result.get("type") == "text":
            return {"type": "text", "content": result["content"]}
        else:
            return result

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
            if os.path.exists(self._temp_dir):
                shutil.rmtree(self._temp_dir)
        except Exception:
            pass

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
