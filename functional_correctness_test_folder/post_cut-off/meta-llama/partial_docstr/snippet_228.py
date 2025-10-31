
import pyperclip
from PIL import Image
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
            if pyperclip.paste().startswith('file://'):
                # Handle file path in clipboard
                return {'type': 'file_path', 'content': pyperclip.paste()[7:]}
            elif pyperclip.paste().isprintable():
                # Handle text in clipboard
                return {'type': 'text', 'content': pyperclip.paste()}
            else:
                # Try to handle image in clipboard
                try:
                    img = Image.frombytes('RGB', (100, 100), pyperclip.paste())
                    return {'type': 'image', 'content': img}
                except Exception as e:
                    return {'success': False, 'error': str(e)}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        try:
            if pyperclip.paste().startswith('file://'):
                # Handle file path in clipboard
                file_path = pyperclip.paste()[7:]
                if os.path.exists(file_path):
                    if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                        img = Image.open(file_path)
                        return {'type': 'image', 'content': img}
                    else:
                        with open(file_path, 'r') as f:
                            return {'type': 'text', 'content': f.read()}
                else:
                    return {'success': False, 'error': 'File not found'}
            else:
                return self.read()
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for file in self.temp_files:
            try:
                os.remove(file)
            except Exception as e:
                print(f"Failed to remove temp file {file}: {e}")
        self.temp_files = []

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
