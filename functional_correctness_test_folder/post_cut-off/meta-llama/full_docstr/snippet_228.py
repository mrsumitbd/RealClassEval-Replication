
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
            tmp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            image.save(tmp_file.name)
            self.temp_files.append(tmp_file.name)
            return tmp_file.name
        except Exception as e:
            print(f"Error creating temp file: {e}")
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
                # Try to get image from clipboard
                try:
                    img = Image.frombytes('RGB', (1, 1), b'\x00\x00\x00')
                    # Not all platforms support image clipboard access via PIL
                    # For simplicity, we assume it's not supported here
                    return {'type': 'unknown', 'content': None}
                except Exception as e:
                    return {'type': 'unknown', 'content': None, 'error': str(e)}
        except Exception as e:
            return {'type': 'unknown', 'content': None, 'error': str(e)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        result = self.read()
        if result.get('type') == 'text':
            return {'type': 'text', 'content': result['content']}
        else:
            # For simplicity, assume we can't directly get image from clipboard
            # In real implementation, you would need to use platform-specific code
            # to access the image from the clipboard
            return {'type': 'unknown', 'content': None}

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for file in self.temp_files:
            try:
                os.remove(file)
            except Exception as e:
                print(f"Error removing temp file {file}: {e}")
        self.temp_files = []

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        self.cleanup_temp_files()
