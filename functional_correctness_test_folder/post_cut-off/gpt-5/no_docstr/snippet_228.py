from typing import Dict, Any, Optional, List
from PIL import Image, ImageGrab
import tempfile
import os


class ClipboardService:

    def __init__(self):
        self._temp_files: List[str] = []

    def _write_text_impl(self, content: str) -> Dict[str, Any]:
        try:
            try:
                import pyperclip  # type: ignore
                pyperclip.copy(content if content is not None else "")
                return {"success": True, "type": "text", "text": content}
            except Exception:
                # Fallback to tkinter
                try:
                    import tkinter as tk  # type: ignore
                    root = tk.Tk()
                    root.withdraw()
                    root.clipboard_clear()
                    root.clipboard_append(
                        content if content is not None else "")
                    root.update_idletasks()
                    root.update()
                    root.destroy()
                    return {"success": True, "type": "text", "text": content}
                except Exception as e2:
                    return {"success": False, "type": "error", "error": f"Failed to write text to clipboard: {e2}"}
        except Exception as e:
            return {"success": False, "type": "error", "error": f"Unexpected error writing text: {e}"}

    def write_text(self, content: str) -> Dict[str, Any]:
        return self._write_text_impl(content)

    def _create_temp_file_from_image(self, image: Image.Image) -> Optional[str]:
        try:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            tmp_path = tmp.name
            tmp.close()
            image.save(tmp_path, format="PNG")
            self._temp_files.append(tmp_path)
            return tmp_path
        except Exception:
            return None

    def read(self) -> Dict[str, Any]:
        try:
            # Try to get image or file list from clipboard
            try:
                data = ImageGrab.grabclipboard()
            except Exception:
                data = None

            if isinstance(data, Image.Image):
                img_path = self._create_temp_file_from_image(data)
                if img_path:
                    return {"success": True, "type": "image", "image_path": img_path}
                else:
                    return {"success": False, "type": "error", "error": "Failed to create temp file for image"}

            if isinstance(data, list):
                files = [p for p in data if isinstance(p, str)]
                return {"success": True, "type": "files", "files": files}

            # Fallback to text
            text_value = None
            text_error = None

            try:
                import pyperclip  # type: ignore
                text_value = pyperclip.paste()
            except Exception:
                try:
                    import tkinter as tk  # type: ignore
                    root = tk.Tk()
                    root.withdraw()
                    try:
                        text_value = root.clipboard_get()
                    finally:
                        root.destroy()
                except Exception as e2:
                    text_error = str(e2)

            if isinstance(text_value, str) and text_value != "":
                return {"success": True, "type": "text", "text": text_value}

            # If everything empty
            if text_error:
                return {"success": False, "type": "empty", "error": f"No clipboard data and failed to read text: {text_error}"}
            return {"success": True, "type": "empty"}
        except Exception as e:
            return {"success": False, "type": "error", "error": f"Unexpected error reading clipboard: {e}"}

        pass

    def read_and_process_paste(self) -> Dict[str, Any]:
        # read already processes image into a temp file
        return self.read()

    def cleanup_temp_files(self):
        for path in list(self._temp_files):
            try:
                if path and os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
            finally:
                try:
                    self._temp_files.remove(path)
                except ValueError:
                    pass

    def write_text(self, content: str) -> Dict[str, Any]:
        return self._write_text_impl(content)

    def __del__(self):
        try:
            self.cleanup_temp_files()
        except Exception:
            pass
