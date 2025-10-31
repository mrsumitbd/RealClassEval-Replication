
import tempfile
import os
from typing import Dict, Any, Optional
from PIL import Image
import pyperclip


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
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                image.save(temp_file.name)
                self.temp_files.append(temp_file.name)
                return temp_file.name
        except Exception as e:
            return None

    def read(self) -> Dict[str, Any]:
        '''
        Read content from the clipboard and automatically determine the content type.
        Returns:
            Dict containing the clipboard content or error information
        '''
        try:
            content = pyperclip.paste()
            return {'content': content, 'type': 'text'}
        except Exception as e:
            return {'error': str(e)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        try:
            content = pyperclip.paste()
            if content.startswith('data:image'):
                # Assuming base64 encoded image
                import base64
                from io import BytesIO
                image_data = content.split(',')[1]
                image = Image.open(BytesIO(base64.b64decode(image_data)))
                temp_file_path = self._create_temp_file_from_image(image)
                if temp_file_path:
                    return {'file_command': f'file://{temp_file_path}'}
            return {'content': content}
        except Exception as e:
            return {'error': str(e)}

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for file_path in self.temp_files:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error cleaning up {file_path}: {e}")
        self.temp_files = []

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
