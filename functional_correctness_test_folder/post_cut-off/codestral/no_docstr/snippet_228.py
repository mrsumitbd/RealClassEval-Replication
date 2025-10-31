
import os
import tempfile
from typing import Dict, Any, Optional
from PIL import Image


class ClipboardService:

    def __init__(self):
        self.temp_files = []

    def write_text(self, content: str) -> Dict[str, Any]:
        import pyperclip
        pyperclip.copy(content)
        return {'status': 'success', 'message': 'Text copied to clipboard'}

    def _create_temp_file_from_image(self, image: Image.Image) -> Optional[str]:
        try:
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, suffix='.png')
            image.save(temp_file.name, format='PNG')
            self.temp_files.append(temp_file.name)
            return temp_file.name
        except Exception as e:
            return None

    def read(self) -> Dict[str, Any]:
        import pyperclip
        content = pyperclip.paste()
        return {'status': 'success', 'content': content}

    def read_and_process_paste(self) -> Dict[str, Any]:
        import pyperclip
        from PIL import ImageGrab

        try:
            image = ImageGrab.grabclipboard()
            if image:
                temp_file_path = self._create_temp_file_from_image(image)
                if temp_file_path:
                    return {'status': 'success', 'type': 'image', 'path': temp_file_path}
                else:
                    return {'status': 'error', 'message': 'Failed to create temporary file from image'}
            else:
                content = pyperclip.paste()
                return {'status': 'success', 'type': 'text', 'content': content}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def cleanup_temp_files(self):
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except Exception as e:
                pass
        self.temp_files = []

    def __del__(self):
        self.cleanup_temp_files()
