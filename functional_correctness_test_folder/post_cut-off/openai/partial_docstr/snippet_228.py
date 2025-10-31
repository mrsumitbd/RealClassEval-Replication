
import os
import tempfile
import shutil
from typing import Any, Dict, Optional, List
from PIL import Image
import pyperclip


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
        try:
            pyperclip.copy(content)
            return {'success': True}
        except Exception as exc:
            return {'success': False, 'error': str(exc)}

    def _create_temp_file_from_image(self, image: Image.Image) -> Optional[str]:
        '''
        Create a temporary file from a PIL Image.
        Args:
            image: PIL Image object
        Returns:
            Path to the temporary file or None if failed
        '''
        try:
            tmp_dir = tempfile.mkdtemp()
            tmp_path = os.path.join(tmp_dir, 'clipboard_image.png')
            image.save(tmp_path, format='PNG')
            self._temp_files.append(tmp_dir)
            return tmp_path
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
            if content is None:
                return {'success': False, 'error': 'No content found'}
            return {'success': True, 'content': content, 'type': 'text'}
        except Exception as exc:
            return {'success': False, 'error': str(exc)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read the clipboard content and process it if it is an image.
        Returns:
            Dict containing the processed content or error information
        '''
        # Currently only supports text; placeholder for image handling
        return self.read()

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for tmp_dir in self._temp_files:
            try:
                shutil.rmtree(tmp_dir)
            except Exception:
                pass
        self._temp_files.clear()

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
