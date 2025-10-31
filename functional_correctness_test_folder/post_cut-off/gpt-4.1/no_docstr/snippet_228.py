
import tempfile
import os
from typing import Dict, Any, Optional, List
from PIL import Image
import io

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    import PIL.ImageGrab as ImageGrab
except ImportError:
    ImageGrab = None


class ClipboardService:

    def __init__(self):
        self._temp_files: List[str] = []

    def write_text(self, content: str) -> Dict[str, Any]:
        if pyperclip is None:
            return {"success": False, "error": "pyperclip not installed"}
        try:
            pyperclip.copy(content)
            return {"success": True, "type": "text", "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _create_temp_file_from_image(self, image: Image.Image) -> Optional[str]:
        try:
            fd, path = tempfile.mkstemp(suffix=".png")
            os.close(fd)
            image.save(path, format="PNG")
            self._temp_files.append(path)
            return path
        except Exception:
            return None

    def read(self) -> Dict[str, Any]:
        if pyperclip is None:
            return {"success": False, "error": "pyperclip not installed"}
        # Try to read text
        try:
            text = pyperclip.paste()
            if isinstance(text, str) and text.strip() != "":
                return {"success": True, "type": "text", "content": text}
        except Exception as e:
            return {"success": False, "error": str(e)}
        # Try to read image (Windows/macOS only)
        if ImageGrab is not None:
            try:
                img = ImageGrab.grabclipboard()
                if isinstance(img, Image.Image):
                    path = self._create_temp_file_from_image(img)
                    return {"success": True, "type": "image", "file": path}
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {"success": False, "error": "Clipboard is empty or unsupported content"}

    def read_and_process_paste(self) -> Dict[str, Any]:
        result = self.read()
        if result.get("type") == "image" and result.get("file"):
            try:
                with Image.open(result["file"]) as img:
                    width, height = img.size
                result["width"] = width
                result["height"] = height
            except Exception:
                pass
        return result

    def cleanup_temp_files(self):
        for path in self._temp_files:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
        self._temp_files.clear()

    def __del__(self):
        self.cleanup_temp_files()
