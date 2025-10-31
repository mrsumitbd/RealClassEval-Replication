
import pyperclip
from PIL import Image, ImageGrab
import tempfile
import os
from typing import Dict, Any, Optional


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
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                image.save(tmp.name)
                self.temp_files.append(tmp.name)
                return tmp.name
        except Exception as e:
            print(f"Failed to create temp file: {e}")
            return None

    def read(self) -> Dict[str, Any]:
        '''
        Read content from the clipboard and automatically determine the content type.
        Returns:
            Dict containing the clipboard content or error information
        '''
        try:
            content = pyperclip.paste()
            if content:
                return {'type': 'text', 'content': content}
            else:
                image = ImageGrab.grabclipboard()
                if isinstance(image, Image.Image):
                    return {'type': 'image', 'content': image}
                elif isinstance(image, list):  # List of file paths
                    return {'type': 'files', 'content': image}
                else:
                    return {'type': 'unknown'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        clipboard_content = self.read()
        if clipboard_content.get('type') == 'text':
            return {'type': 'text', 'content': clipboard_content['content']}
        elif clipboard_content.get('type') == 'image':
            image_path = self._create_temp_file_from_image(
                clipboard_content['content'])
            if image_path:
                return {'type': 'file', 'path': image_path}
        elif clipboard_content.get('type') == 'files':
            # Assuming the first file is the one we're interested in
            file_path = clipboard_content['content'][0]
            return {'type': 'file', 'path': file_path}
        return {'type': 'unknown'}

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for file_path in self.temp_files:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to remove {file_path}: {e}")
        self.temp_files = []

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
