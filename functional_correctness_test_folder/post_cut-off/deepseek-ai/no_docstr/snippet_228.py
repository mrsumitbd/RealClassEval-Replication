
import os
import tempfile
from typing import Dict, Any, Optional
from PIL import Image
import pyperclip


class ClipboardService:

    def __init__(self):
        self._temp_files = []

    def write_text(self, content: str) -> Dict[str, Any]:
        try:
            pyperclip.copy(content)
            return {"status": "success", "message": "Text copied to clipboard"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _create_temp_file_from_image(self, image: Image.Image) -> Optional[str]:
        try:
            temp_file = tempfile.NamedTemporaryFile(
                suffix=".png", delete=False)
            image.save(temp_file.name, format="PNG")
            self._temp_files.append(temp_file.name)
            return temp_file.name
        except Exception:
            return None

    def read(self) -> Dict[str, Any]:
        try:
            content = pyperclip.paste()
            return {"status": "success", "content": content, "type": "text"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        try:
            if pyperclip.is_available():
                content = pyperclip.paste()
                if content:
                    return {"status": "success", "content": content, "type": "text"}
                else:
                    return {"status": "empty", "message": "Clipboard is empty"}
            else:
                return {"status": "error", "message": "Clipboard not available"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def cleanup_temp_files(self):
        for file_path in self._temp_files:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception:
                pass
        self._temp_files = []

    def __del__(self):
        self.cleanup_temp_files()
