import os
import io
import sys
import shutil
import tempfile
import platform
import subprocess
from typing import Dict, Any, Optional, List, Tuple

try:
    import pyperclip  # type: ignore
except Exception:
    pyperclip = None

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
        self._os = platform.system().lower()

    def _read_text(self) -> Tuple[Optional[str], Optional[str]]:
        # Try pyperclip first
        if pyperclip is not None:
            try:
                return pyperclip.paste(), None
            except Exception as e:
                pass
        # macOS
        if self._os == 'darwin':
            try:
                p = subprocess.run(
                    ['pbpaste'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                return p.stdout.decode('utf-8', errors='ignore'), None
            except Exception as e:
                return None, str(e)
        # Windows
        if self._os == 'windows':
            try:
                # Use PowerShell Get-Clipboard for reliability
                p = subprocess.run(['powershell', '-NoProfile', '-Command', 'Get-Clipboard'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                return p.stdout.decode('utf-8', errors='ignore'), None
            except Exception as e:
                return None, str(e)
        # Linux/other
        try:
            if shutil.which('xclip'):
                p = subprocess.run(['xclip', '-selection', 'clipboard', '-o'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                return p.stdout.decode('utf-8', errors='ignore'), None
            if shutil.which('xsel'):
                p = subprocess.run(
                    ['xsel', '-b', '-o'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                return p.stdout.decode('utf-8', errors='ignore'), None
        except Exception as e:
            return None, str(e)
        return None, 'No clipboard text backend available'

    def _read_image_pil(self) -> Tuple[Optional["Image.Image"], Optional[str]]:
        if Image is None:
            return None, 'Pillow is not available'
        # Try ImageGrab.grabclipboard on Windows/macOS
        if ImageGrab is not None and self._os in ('windows', 'darwin'):
            try:
                data = ImageGrab.grabclipboard()
                if hasattr(data, 'mode'):
                    return data, None  # PIL Image
                if isinstance(data, list):
                    # List of file paths; if they are images, open the first
                    for pth in data:
                        try:
                            img = Image.open(pth)
                            return img, None
                        except Exception:
                            continue
            except Exception as e:
                return None, str(e)
        # Linux path via xclip image/png
        if self._os not in ('windows', 'darwin'):
            try:
                if shutil.which('xclip'):
                    p = subprocess.run(['xclip', '-selection', 'clipboard', '-t',
                                       'image/png', '-o'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if p.returncode == 0 and p.stdout:
                        try:
                            img = Image.open(io.BytesIO(p.stdout))
                            return img, None
                        except Exception as e:
                            return None, str(e)
                if shutil.which('xsel'):
                    # xsel doesn't directly support mime types; try primary binary read (best-effort)
                    p = subprocess.run(
                        ['xsel', '-b', '-o'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if p.returncode == 0 and p.stdout:
                        try:
                            img = Image.open(io.BytesIO(p.stdout))
                            return img, None
                        except Exception:
                            pass
            except Exception as e:
                return None, str(e)
        return None, 'No image found in clipboard'

    def _read_file_list(self) -> Tuple[Optional[List[str]], Optional[str]]:
        # Windows/mac via ImageGrab.grabclipboard can return list of file paths
        if ImageGrab is not None and self._os in ('windows', 'darwin'):
            try:
                data = ImageGrab.grabclipboard()
                if isinstance(data, list):
                    paths = [p for p in data if isinstance(p, str)]
                    if paths:
                        return paths, None
            except Exception as e:
                return None, str(e)
        # Other platforms: no general file-path clipboard standard available
        return None, 'No file paths available from clipboard'

    def _guess_ext_and_mime_from_bytes(self, data: bytes) -> Tuple[str, str]:
        # Minimal magic number inference
        if data.startswith(b'\x89PNG\r\n\x1a\n'):
            return '.png', 'image/png'
        if data[:3] == b'\xff\xd8\xff':
            return '.jpg', 'image/jpeg'
        if data[:2] == b'BM':
            return '.bmp', 'image/bmp'
        if data[:4] == b'GIF8':
            return '.gif', 'image/gif'
        if data[:4] == b'%PDF':
            return '.pdf', 'application/pdf'
        return '.bin', 'application/octet-stream'

    def _create_temp_file_from_image(self, image: "Image.Image") -> Optional[str]:
        '''
        Create a temporary file from a PIL Image.
        Args:
            image: PIL Image object
        Returns:
            Path to the temporary file or None if failed
        '''
        if Image is None or image is None:
            return None
        try:
            fd, path = tempfile.mkstemp(
                suffix='.png', prefix='clip_', text=False)
            os.close(fd)
            image.save(path, format='PNG')
            self._temp_files.append(path)
            return path
        except Exception:
            return None

    def read(self) -> Dict[str, Any]:
        '''
        Read content from the clipboard and automatically determine the content type.
        Returns:
            Dict containing the clipboard content or error information
        '''
        # Try image
        img, img_err = self._read_image_pil()
        if img is not None:
            return {'ok': True, 'type': 'image', 'image': img}
        # Try file list
        files, files_err = self._read_file_list()
        if files:
            return {'ok': True, 'type': 'files', 'files': files}
        # Try text
        text, txt_err = self._read_text()
        if text is not None and text != '':
            return {'ok': True, 'type': 'text', 'text': text}
        # If all failed, craft error message
        err_msgs = [m for m in [img_err, files_err, txt_err] if m]
        return {'ok': False, 'error': '; '.join(err_msgs) if err_msgs else 'Clipboard read failed'}

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
            if path:
                return {
                    'ok': True,
                    'type': 'file',
                    'path': path,
                    'mimetype': 'image/png',
                    'command': f'file:{path}',
                    'source': 'clipboard'
                }
            return {'ok': False, 'error': 'Failed to create temp file from image'}

        if ctype == 'files':
            files = result.get('files', [])
            if not files:
                return {'ok': False, 'error': 'Empty file list from clipboard'}
            # Return all paths; primary_path is the first
            return {
                'ok': True,
                'type': 'files',
                'paths': files,
                'primary_path': files[0],
                'command': f'file:{files[0]}',
                'source': 'clipboard'
            }

        if ctype == 'text':
            text = result.get('text', '')
            return {'ok': True, 'type': 'text', 'text': text}

        # Fallback for unknown types
        return {'ok': False, 'error': f'Unhandled clipboard content type: {ctype}'}

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        to_delete = list(self._temp_files)
        self._temp_files.clear()
        for p in to_delete:
            try:
                if p and os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass

    def write_text(self, content: str) -> Dict[str, Any]:
        '''
        Write content to the clipboard.
        Args:
            content: Content to write to clipboard
        Returns:
            Dict containing success status and any error information
        '''
        # Try pyperclip
        if pyperclip is not None:
            try:
                pyperclip.copy(content if content is not None else '')
                return {'ok': True}
            except Exception as e:
                pass
        # macOS
        if self._os == 'darwin':
            try:
                p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
                p.communicate(input=(content or '').encode('utf-8'))
                if p.returncode == 0:
                    return {'ok': True}
                return {'ok': False, 'error': 'pbcopy returned non-zero'}
            except Exception as e:
                return {'ok': False, 'error': str(e)}
        # Windows
        if self._os == 'windows':
            try:
                # clip expects UTF-16LE. Ensure trailing newline to flush properly.
                data = (content or '') + '\r\n'
                p = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
                p.communicate(input=data.encode('utf-16le'))
                if p.returncode == 0:
                    return {'ok': True}
                return {'ok': False, 'error': 'clip returned non-zero'}
            except Exception as e:
                # Fallback to PowerShell
                try:
                    ps_cmd = f'Set-Clipboard -Value @\'\n{content or ""}\n\'@'
                    subprocess.run(['powershell', '-NoProfile',
                                   '-Command', ps_cmd], check=True)
                    return {'ok': True}
                except Exception as e2:
                    return {'ok': False, 'error': f'{e}; {e2}'}
        # Linux/other
        try:
            data = (content or '').encode('utf-8')
            if shutil.which('xclip'):
                p = subprocess.Popen(
                    ['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                p.communicate(input=data)
                if p.returncode == 0:
                    return {'ok': True}
            if shutil.which('xsel'):
                p = subprocess.Popen(['xsel', '-b', '-i'],
                                     stdin=subprocess.PIPE)
                p.communicate(input=data)
                if p.returncode == 0:
                    return {'ok': True}
            return {'ok': False, 'error': 'No clipboard utility (xclip/xsel) available'}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        try:
            self.cleanup_temp_files()
        except Exception:
            pass
