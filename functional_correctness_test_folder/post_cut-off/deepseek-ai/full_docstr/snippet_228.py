
import os
import tempfile
from typing import Dict, Any, Optional
from PIL import Image
import pyperclip
import shutil


class ClipboardService:
    '''Service for interacting with the system clipboard.'''

    def __init__(self):
        '''Initialize the clipboard service.'''
        self._temp_files = []

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
            temp_dir = tempfile.mkdtemp()
            temp_file = os.path.join(temp_dir, 'clipboard_image.png')
            image.save(temp_file, 'PNG')
            self._temp_files.append(temp_file)
            return temp_file
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
            return {'success': True, 'content': content, 'type': 'text'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        try:
            if pyperclip.is_available():
                if hasattr(pyperclip, 'paste_image'):
                    image = pyperclip.paste_image()
                    if image:
                        temp_file = self._create_temp_file_from_image(image)
                        if temp_file:
                            return {'success': True, 'type': 'file', 'path': temp_file}
                text = pyperclip.paste()
                return {'success': True, 'type': 'text', 'content': text}
            return {'success': False, 'error': 'Clipboard not available'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for temp_file in self._temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                temp_dir = os.path.dirname(temp_file)
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except Exception:
                pass
        self._temp_files = []

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
