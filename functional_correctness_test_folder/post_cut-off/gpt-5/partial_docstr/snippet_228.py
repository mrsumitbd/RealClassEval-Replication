from typing import Dict, Any, Optional, List
import os
import shutil
import tempfile

try:
    from PIL import Image, ImageGrab
except Exception:  # Pillow not installed or ImageGrab unsupported
    Image = None  # type: ignore
    ImageGrab = None  # type: ignore

try:
    import pyperclip
    from pyperclip import PyperclipException
except Exception:
    pyperclip = None  # type: ignore
    PyperclipException = Exception  # type: ignore


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
        # This method will be overridden by the definition below (Python keeps the last definition).
        return {"success": False, "error": "Method overridden by later definition."}

    def _create_temp_file_from_image(self, image: Image.Image) -> Optional[str]:
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
            fd, path = tempfile.mkstemp(suffix=".png", prefix="clipboard_img_")
            os.close(fd)
            image.save(path, format="PNG")
            self._temp_files.append(path)
            return path
        except Exception:
            # Cleanup partially created file
            try:
                if 'path' in locals() and os.path.exists(path):
                    os.unlink(path)
            except Exception:
                pass
            return None

    def _try_read_image_from_clipboard(self) -> Dict[str, Any]:
        if ImageGrab is None:
            return {"success": False, "error": "Image clipboard not supported: PIL.ImageGrab unavailable."}
        try:
            clip = ImageGrab.grabclipboard()
        except Exception as e:
            return {"success": False, "error": f"Failed to access clipboard for image: {e}"}

        if clip is None:
            return {"success": True, "type": "empty", "data": None}

        # If it's an image
        if Image is not None and isinstance(clip, Image.Image):
            path = self._create_temp_file_from_image(clip)
            if path:
                return {"success": True, "type": "image", "data": {"path": path, "format": "PNG"}}
            return {"success": False, "error": "Failed to create temp file from clipboard image."}

        # If it's a list of file paths
        if isinstance(clip, list) and all(isinstance(p, str) for p in clip):
            # Normalize paths
            files = []
            for p in clip:
                try:
                    files.append(os.path.abspath(p))
                except Exception:
                    files.append(p)
            return {"success": True, "type": "files", "data": {"files": files}}

        return {"success": True, "type": "unknown", "data": clip}

    def _try_read_text_from_clipboard(self) -> Dict[str, Any]:
        if pyperclip is None:
            return {"success": False, "error": "pyperclip is not installed."}
        try:
            text = pyperclip.paste()
            if text is None:
                return {"success": True, "type": "empty", "data": None}
            return {"success": True, "type": "text", "data": {"text": text}}
        except PyperclipException as e:
            return {"success": False, "error": f"Clipboard text not available: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to read text from clipboard: {e}"}

    def read(self) -> Dict[str, Any]:
        '''
        Read content from the clipboard and automatically determine the content type.
        Returns:
            Dict containing the clipboard content or error information
        '''
        # Prefer image/files first, then text, to avoid losing binary clipboard content
        img_res = self._try_read_image_from_clipboard()
        if img_res.get("success"):
            t = img_res.get("type")
            if t in ("image", "files", "unknown"):
                return img_res
            # If empty, still check text
        elif img_res.get("error"):
            # Continue to text even if image read failed (platforms without ImageGrab)
            pass

        text_res = self._try_read_text_from_clipboard()
        if text_res.get("success"):
            return text_res

        # If both failed, return a combined error
        return {
            "success": False,
            "error": f"Image read error: {img_res.get('error')}; Text read error: {text_res.get('error')}",
        }

    def read_and_process_paste(self) -> Dict[str, Any]:
        res = self.read()
        if not res.get("success"):
            return res

        rtype = res.get("type")
        data = res.get("data")

        if rtype == "files" and isinstance(data, dict):
            files = data.get("files", [])
            if isinstance(files, list) and files:
                # If a single image file, normalize as image_file
                img_exts = {".png", ".jpg", ".jpeg", ".gif",
                            ".bmp", ".webp", ".tif", ".tiff", ".ico"}
                first = files[0]
                _, ext = os.path.splitext(first.lower())
                if ext in img_exts and os.path.isfile(first):
                    return {"success": True, "type": "image_file", "data": {"path": first}}
                return {"success": True, "type": "files", "data": {"files": files}}
            return {"success": True, "type": "files", "data": {"files": []}}

        # Pass-through for text/image/unknown/empty
        return res

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for path in list(self._temp_files):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
                elif os.path.exists(path):
                    os.unlink(path)
            except Exception:
                pass
            finally:
                try:
                    self._temp_files.remove(path)
                except ValueError:
                    pass

    def write_text(self, content: str) -> Dict[str, Any]:
        '''
        Write content to the clipboard.
        Args:
            content: Content to write to clipboard
        Returns:
            Dict containing success status and any error information
        '''
        if pyperclip is None:
            return {"success": False, "error": "pyperclip is not installed."}
        try:
            pyperclip.copy("" if content is None else str(content))
            return {"success": True}
        except PyperclipException as e:
            return {"success": False, "error": f"Failed to write to clipboard: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error writing to clipboard: {e}"}

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        try:
            self.cleanup_temp_files()
        except Exception:
            pass
