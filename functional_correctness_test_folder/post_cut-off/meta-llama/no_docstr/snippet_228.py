
import pyperclip
from PIL import Image
import tempfile
import os
from typing import Dict, Any, Optional


class ClipboardService:

    def __init__(self):
        self.temp_files = []

    def write_text(self, content: str) -> Dict[str, Any]:
        try:
            pyperclip.copy(content)
            return {"success": True, "message": "Text copied to clipboard"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def _create_temp_file_from_image(self, image: Image.Image) -> Optional[str]:
        try:
            temp_file = tempfile.NamedTemporaryFile(
                suffix=".png", delete=False)
            image.save(temp_file.name)
            self.temp_files.append(temp_file.name)
            return temp_file.name
        except Exception as e:
            print(f"Error creating temp file: {e}")
            return None

    def read(self) -> Dict[str, Any]:
        try:
            text = pyperclip.paste()
            return {"type": "text", "content": text}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        try:
            if pyperclip.is_image_available():
                image = pyperclip.paste_image()
                temp_file_path = self._create_temp_file_from_image(image)
                if temp_file_path:
                    return {"type": "image", "content": temp_file_path}
                else:
                    return {"success": False, "message": "Failed to process image"}
            else:
                text = pyperclip.paste()
                return {"type": "text", "content": text}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def cleanup_temp_files(self):
        for file_path in self.temp_files:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting temp file {file_path}: {e}")
        self.temp_files = []

    def __del__(self):
        self.cleanup_temp_files()
