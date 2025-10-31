from typing import Any, Dict, Optional, List
import os
import shutil
import tempfile
import uuid

try:
    import pyperclip  # type: ignore
except Exception:
    pyperclip = None

try:
    from PIL import Image, ImageGrab  # type: ignore
except Exception:
    Image = None
    ImageGrab = None


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
        if not isinstance(content, str):
            return {"success": False, "error": "content must be a string"}
        if pyperclip is None:
            return {"success": False, "error": "pyperclip not available"}
        try:
            pyperclip.copy(content)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _create_temp_file_from_image(self, image: "Image.Image") -> Optional[str]:
        '''
        Create a temporary file from a PIL Image.
        Args:
            image: PIL Image object
        Returns:
            Path to the temporary file or None if failed
        '''
        if Image is None or image is None:
            return None
        try:
            tmp_dir = tempfile.gettempdir()
            filename = f"clipboard_img_{uuid.uuid4().hex}.png"
            path = os.path.join(tmp_dir, filename)
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
        # Try image or file list via ImageGrab.grabclipboard
        if ImageGrab is not None:
            try:
                grabbed = ImageGrab.grabclipboard()
                # grabbed can be None, PIL.Image.Image, or a list of file paths
                if grabbed is None:
                    pass
                elif Image is not None and isinstance(grabbed, Image.Image):
                    return {"success": True, "type": "image"}
                elif isinstance(grabbed, list) and all(isinstance(p, str) for p in grabbed):
                    # List of file paths from clipboard (Windows/Mac)
                    return {"success": True, "type": "files", "paths": grabbed}
            except Exception:
                # Fall back to text if image/file grab fails
                pass

        # Fallback: read text
        if pyperclip is None:
            return {"success": False, "error": "No clipboard backend available (pyperclip not installed)"}
        try:
            text = pyperclip.paste()
            # Some environments may return None; normalize to empty string
            if text is None:
                text = ""
            return {"success": True, "type": "text", "content": text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        # Try image or file list
        if ImageGrab is not None:
            try:
                grabbed = ImageGrab.grabclipboard()
                if grabbed is None:
                    pass
                elif Image is not None and isinstance(grabbed, Image.Image):
                    path = self._create_temp_file_from_image(grabbed)
                    if path:
                        return {"success": True, "type": "file", "path": path}
                    return {"success": False, "error": "Failed to create temp file from image"}
                elif isinstance(grabbed, list) and all(isinstance(p, str) for p in grabbed):
                    # Return first file path (common behavior for pasting a single file)
                    if len(grabbed) > 0:
                        path = grabbed[0]
                        # If it's an existing file, just return the path; do not copy to temp
                        if os.path.isfile(path):
                            return {"success": True, "type": "file", "path": path}
                        # If it's a directory or non-file, return error
                        return {"success": False, "error": "Clipboard contains non-file paths"}
            except Exception:
                # Fall through to text
                pass

        # Fallback to text
        if pyperclip is None:
            return {"success": False, "error": "No clipboard backend available (pyperclip not installed)"}
        try:
            text = pyperclip.paste()
            if text is None:
                text = ""
            return {"success": True, "type": "text", "content": text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        remaining: List[str] = []
        for path in self._temp_files:
            try:
                if os.path.isfile(path):
                    os.remove(path)
            except Exception:
                remaining.append(path)
        self._temp_files = remaining

    def write_text(self, content: str) -> Dict[str, Any]:
        '''
        Write content to the clipboard.
        Args:
            content: Content to write to clipboard
        Returns:
            Dict containing success status and any error information
        '''
        return self.write_text.__wrapped__(self, content)  # type: ignore[attr-defined]

    # Preserve the original implementation for the duplicate method
    # Assign __wrapped__ so the redefined method can call it
    write_text.__wrapped__ = lambda self, content: (
        {"success": False, "error": "content must be a string"}
        if not isinstance(content, str)
        else (
            {"success": False, "error": "pyperclip not available"}
            if pyperclip is None
            else (lambda: (pyperclip.copy(content), {"success": True}))()[1]
        )
    )  # type: ignore

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        try:
            self.cleanup_temp_files()
        except Exception:
            pass
