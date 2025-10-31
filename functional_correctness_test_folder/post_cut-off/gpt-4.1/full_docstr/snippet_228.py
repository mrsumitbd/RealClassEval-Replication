
import os
import tempfile
import shutil
from typing import Dict, Any, Optional, List
from PIL import Image
import pyperclip

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
            text = pyperclip.paste()
            if text:
                return {"type": "text", "content": text}
        except Exception as e:
            return {"success": False, "error": f"Text read error: {e}"}

        # Try image (if tkinter is available)
        if tk is not None:
            try:
                root = tk.Tk()
                root.withdraw()
                img = None
                try:
                    img = root.clipboard_get(type='image')
                except Exception:
                    pass
                if img:
                    # Not a PIL Image, so try to get as bytes
                    # This is platform dependent and not always supported
                    # So we skip this for now
                    pass
                root.destroy()
            except Exception:
                pass

        return {"success": False, "error": "No supported clipboard content found."}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        # Try text first
        try:
            text = pyperclip.paste()
            if text:
                return {"type": "text", "content": text}
        except Exception as e:
            return {"success": False, "error": f"Text read error: {e}"}

        # Try image (if tkinter and PIL are available)
        if tk is not None:
            try:
                root = tk.Tk()
                root.withdraw()
                try:
                    # Try to get image from clipboard
                    img_data = root.clipboard_get(type='image')
                except Exception:
                    img_data = None
                root.destroy()
                if img_data:
                    # Not a PIL Image, so try to get as bytes
                    # This is platform dependent and not always supported
                    # So we skip this for now
                    pass
            except Exception:
                pass

        return {"success": False, "error": "No supported clipboard content found."}

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
