
import os
import tempfile
from typing import Dict, Any, Optional
from PIL import Image
import pyperclip
import base64
import io


class ClipboardService:
    '''Service for interacting with the system clipboard.'''

    def __init__(self):
        '''Initialize the clipboard service.'''
        self.temp_files = []

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
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _create_temp_file_from_image(self, image: Image.Image) -> Optional[str]:
        '''
        Create a temporary file from a PIL Image.
        Args:
            image: PIL Image object
        Returns:
            Path to the temporary file or None if failed
        '''
        try:
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, suffix='.png')
            image.save(temp_file.name, format='PNG')
            self.temp_files.append(temp_file.name)
            return temp_file.name
        except Exception:
            return None

    def read(self) -> Dict[str, Any]:
        '''
        Read content from the clipboard and automatically determine the content type.
        Returns:
            Dict containing the clipboard content or error information
        '''
        try:
            content = pyperclip.paste()
            if content.startswith('data:image/'):
                # Handle base64 encoded image
                header, encoded = content.split(',', 1)
                image_data = base64.b64decode(encoded)
                image = Image.open(io.BytesIO(image_data))
                temp_path = self._create_temp_file_from_image(image)
                if temp_path:
                    return {'type': 'image', 'path': temp_path}
                else:
                    return {'type': 'text', 'content': content}
            else:
                return {'type': 'text', 'content': content}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        result = self.read()
        if result.get('type') == 'image':
            return {'type': 'file', 'command': f'file {result["path"]}'}
        elif result.get('type') == 'text':
            return {'type': 'text', 'content': result['content']}
        else:
            return {'type': 'error', 'message': result.get('error', 'Unknown error')}

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for file_path in self.temp_files:
            try:
                os.unlink(file_path)
            except Exception:
                pass
        self.temp_files = []

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
