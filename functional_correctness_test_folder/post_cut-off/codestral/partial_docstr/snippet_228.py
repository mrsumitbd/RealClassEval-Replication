
import os
import tempfile
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
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, suffix='.png')
            image.save(temp_file, format='PNG')
            temp_file_path = temp_file.name
            temp_file.close()
            self.temp_files.append(temp_file_path)
            return temp_file_path
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
            return {'success': True, 'content': content, 'content_type': 'text'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        pass

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except Exception:
                pass
        self.temp_files = []

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
