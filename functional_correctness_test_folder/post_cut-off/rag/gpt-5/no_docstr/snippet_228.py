from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, List

try:
    import pyperclip  # type: ignore
except Exception:
    pyperclip = None  # type: ignore

try:
    from tkinter import Tk  # type: ignore
except Exception:
    Tk = None  # type: ignore

try:
    from PIL import Image, ImageGrab  # type: ignore
except Exception:
    Image = None  # type: ignore
    ImageGrab = None  # type: ignore


class ClipboardService:
    '''Service for interacting with the system clipboard.'''

    def __init__(self):
        '''Initialize the clipboard service.'''
        self._temp_files: List[str] = []

    def _write_text_impl(self, content: str) -> Dict[str, Any]:
        try:
            if not isinstance(content, str):
                return {'ok': False, 'error': 'Content must be a string.'}
            if pyperclip:
                pyperclip.copy(content)
                return {'ok': True}
            if Tk is None:
                return {'ok': False, 'error': 'No clipboard backend available (pyperclip/tkinter not found).'}
            root = Tk()
            try:
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(content)
                root.update()
            finally:
                try:
                    root.destroy()
                except Exception:
                    pass
            return {'ok': True}
        except Exception as e:
            return {'ok': False, 'error': str(e), 'exception': repr(e)}

    def write_text(self, content: str) -> Dict[str, Any]:
        '''
        Write text content to the clipboard.
        Args:
            content: Text content to write to clipboard
        Returns:
            Dict containing success status and any error information
        '''
        return self._write_text_impl(content)

    def _create_temp_file_from_image(self, image: Image.Image) -> Optional[str]:
        '''
        Create a temporary file from a PIL Image.
        Args:
            image: PIL Image object
        Returns:
            Path to the temporary file or None if failed
        '''
        try:
            if Image is None or image is None:
                return None
            fd, path = tempfile.mkstemp(suffix='.png')
            os.close(fd)
            image.save(path, format='PNG')
            self._temp_files.append(path)
            return path
        except Exception:
            return None

    def _read_text(self) -> Dict[str, Any]:
        try:
            text: Optional[str] = None
            if pyperclip:
                text = pyperclip.paste()
            elif Tk is not None:
                root = Tk()
                try:
                    root.withdraw()
                    text = root.clipboard_get()
                finally:
                    try:
                        root.destroy()
                    except Exception:
                        pass
            else:
                return {'ok': False, 'error': 'No clipboard backend available (pyperclip/tkinter not found).'}
            if text is None:
                return {'ok': False, 'error': 'No text available on clipboard.'}
            return {'ok': True, 'type': 'text', 'text': text}
        except Exception as e:
            return {'ok': False, 'error': str(e), 'exception': repr(e)}

    def read(self) -> Dict[str, Any]:
        '''
        Read content from the clipboard and automatically determine the content type.
        Returns:
            Dict containing the clipboard content or error information
        '''
        try:
            if ImageGrab is not None:
                grabbed = None
                try:
                    grabbed = ImageGrab.grabclipboard()
                except Exception:
                    grabbed = None
                if grabbed is not None:
                    if Image is not None and isinstance(grabbed, Image.Image):
                        return {'ok': True, 'type': 'image', 'image': grabbed}
                    if isinstance(grabbed, list) and grabbed and all(isinstance(p, str) for p in grabbed):
                        return {'ok': True, 'type': 'files', 'files': grabbed}
            return self._read_text()
        except Exception as e:
            return {'ok': False, 'error': str(e), 'exception': repr(e)}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        result = self.read()
        if not result.get('ok'):
            return result
        ctype = result.get('type')
        if ctype == 'image':
            img = result.get('image')
            path = self._create_temp_file_from_image(img)
            if not path:
                return {'ok': False, 'error': 'Failed to create temporary image file.'}
            uri = Path(path).as_uri()
            return {
                'ok': True,
                'type': 'file',
                'file_path': path,
                'file_uri': uri,
                'file_command': uri
            }
        if ctype == 'files':
            files = result.get('files', [])
            if not files:
                return {'ok': False, 'error': 'Clipboard contained empty file list.'}
            uris = []
            for f in files:
                try:
                    uris.append(Path(f).resolve().as_uri())
                except Exception:
                    uris.append(f'file://{f}')
            return {
                'ok': True,
                'type': 'files',
                'file_paths': files,
                'file_uris': uris,
                'file_commands': uris
            }
        return result

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        for path in list(self._temp_files):
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
            finally:
                try:
                    self._temp_files.remove(path)
                except ValueError:
                    pass

    def write_text(self, content: str) -> Dict[str, Any]:
        '''
        Write content to the clipboard.
        Args:
            content: Content to write to clipboard
        Returns:
            Dict containing success status and any error information
        '''
        return self._write_text_impl(content)

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        try:
            self.cleanup_temp_files()
        except Exception:
            pass
