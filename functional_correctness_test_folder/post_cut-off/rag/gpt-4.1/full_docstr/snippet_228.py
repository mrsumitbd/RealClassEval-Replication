
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
    import tkinter
except ImportError:
    tkinter = None


class ClipboardService:
    '''Service for interacting with the system clipboard.'''

    def __init__(self):
        '''Initialize the clipboard service.'''
        self._temp_files = []
        self._temp_dir = tempfile.mkdtemp(prefix="clipboard_service_")

    def write_text(self, content: str) -> Dict[str, Any]:
        '''
        Write text content to the clipboard.
        Args:
            content: Text content to write to clipboard
        Returns:
            Dict containing success status and any error information
        '''
        result = {"success": False, "error": None}
        try:
            if pyperclip:
                pyperclip.copy(content)
                result["success"] = True
            elif tkinter:
                root = tkinter.Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(content)
                root.update()
                root.destroy()
                result["success"] = True
            else:
                result["error"] = "No clipboard library available (pyperclip or tkinter required)."
        except Exception as e:
            result["error"] = str(e)
        return result

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
        result = {"success": False, "type": None,
                  "content": None, "error": None}
        try:
            # Try text first
            text = None
            if pyperclip:
                text = pyperclip.paste()
            elif tkinter:
                root = tkinter.Tk()
                root.withdraw()
                try:
                    text = root.clipboard_get()
                except Exception:
                    text = None
                root.destroy()
            if text:
                result["success"] = True
                result["type"] = "text"
                result["content"] = text
                return result
            # Try image (PIL + tkinter)
            if tkinter and Image:
                root = tkinter.Tk()
                root.withdraw()
                try:
                    img = None
                    if sys.platform == "win32":
                        # Windows: use tkinter image grab
                        from PIL import ImageGrab
                        img = ImageGrab.grabclipboard()
                    else:
                        # On Linux/Mac, try to get image from clipboard (not always supported)
                        pass
                    if img and isinstance(img, Image.Image):
                        result["success"] = True
                        result["type"] = "image"
                        result["content"] = img
                        return result
                except Exception:
                    pass
                finally:
                    root.destroy()
            result["error"] = "Clipboard is empty or unsupported content type."
        except Exception as e:
            result["error"] = str(e)
        return result

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        result = {"success": False, "type": None,
                  "content": None, "file_path": None, "error": None}
        read_result = self.read()
        if not read_result["success"]:
            return read_result
        if read_result["type"] == "text":
            result["success"] = True
            result["type"] = "text"
            result["content"] = read_result["content"]
            return result
        elif read_result["type"] == "image":
            img = read_result["content"]
            file_path = self._create_temp_file_from_image(img)
            if file_path:
                result["success"] = True
                result["type"] = "file"
                result["file_path"] = file_path
                result["content"] = f"file://{file_path}"
            else:
                result["error"] = "Failed to create temp file from image."
            return result
        else:
            result["error"] = "Unsupported clipboard content type."
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
        try:
            if os.path.exists(self._temp_dir):
                shutil.rmtree(self._temp_dir)
        except Exception:
            pass

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
