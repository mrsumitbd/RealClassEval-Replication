
import os
import tempfile
import shutil
from typing import Any, Dict, Optional, List
import pyperclip
from PIL import Image, ImageGrab


class ClipboardService:
    '''Service for interacting with the system clipboard.'''

    def __init__(self):
        '''Initialize the clipboard service.'''
        self._temp_files: List[str] = []

    def write_text(self, content: str) -> Dict[str, Any]:
        '''
        Write text content to the clipboard.
        Args:
            content: Text content to write to clipboard
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
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            image.save(tmp.name, format="PNG")
            tmp.close()
            self._temp_files.append(tmp.name)
            return tmp.name
        except Exception:
            return None

    def read(self) -> Dict[str, Any]:
        '''
        Read content from the clipboard and automatically determine the content type.
        Returns:
            Dict containing the clipboard content or error information
        '''
        try:
            # Try to get image or file list first
            result = ImageGrab.grabclipboard()
            if isinstance(result, Image.Image):
                # Image found
                temp_path = self._create_temp_file_from_image(result)
                if temp_path:
                    return {"type": "image", "path": temp_path}
                else:
                    return {"type": "image", "error": "Failed to create temp file"}
            if isinstance(result, list):
                # List of file paths
                files = []
                for path in result:
                    if os.path.isfile(path):
                        files.append(path)
                return {"type": "files", "paths": files}
            # Fallback to text
            text = pyperclip.paste()
            return {"type": "text", "content": text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        data = self.read()
        if data.get("type") == "image" and "path" in data:
            return {"command": "process_file", "path": data["path"]}
        if data.get("type") == "files" and data.get("paths"):
            # For simplicity, just return the first file
            return {"command": "process_file", "path": data["paths"][0]}
        if data.get("type") == "text":
            return {"text": data["content"]}
        return {"error": "Unsupported clipboard content"}

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for path in self._temp_files:
            try:
                os.remove(path)
            except Exception:
                pass
        self._temp_files.clear()

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
