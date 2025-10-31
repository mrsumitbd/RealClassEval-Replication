from typing import Dict, Any, Optional, List
import os
import sys
import tempfile
import subprocess
from pathlib import Path

try:
    from PIL import Image, ImageGrab
except Exception:  # PIL not available or ImageGrab unsupported
    Image = None  # type: ignore
    ImageGrab = None  # type: ignore

try:
    import pyperclip  # type: ignore
except Exception:
    pyperclip = None  # type: ignore

try:
    import tkinter as tk  # type: ignore
    from tkinter import TclError  # type: ignore
except Exception:
    tk = None  # type: ignore
    TclError = Exception  # type: ignore


class ClipboardService:
    '''Service for interacting with the system clipboard.'''

    def __init__(self):
        '''Initialize the clipboard service.'''
        self._temp_files: List[str] = []
        self._platform = sys.platform

    def write_text(self, content: str) -> Dict[str, Any]:
        '''
        Write text content to the clipboard.
        Args:
            content: Text content to write to clipboard
        Returns:
            Dict containing success status and any error information
        '''
        try:
            if pyperclip is not None:
                pyperclip.copy(content)
                return {"success": True, "backend": "pyperclip"}
        except Exception as e:
            last_err = str(e)
        else:
            last_err = ""

        try:
            if tk is not None:
                root = tk.Tk()
                try:
                    root.withdraw()
                    root.clipboard_clear()
                    root.clipboard_append(content)
                    root.update()
                    return {"success": True, "backend": "tkinter"}
                finally:
                    try:
                        root.destroy()
                    except Exception:
                        pass
        except Exception as e:
            last_err = str(e)

        try:
            if self._platform == "darwin":
                subprocess.run(
                    ["pbcopy"], input=content.encode("utf-8"), check=True)
                return {"success": True, "backend": "pbcopy"}
            elif self._platform.startswith("win"):
                # Use clip
                subprocess.run("clip", input=content.encode(
                    "utf-16le"), check=True, shell=True)
                return {"success": True, "backend": "clip"}
            else:
                # Try xclip, then xsel
                try:
                    subprocess.run(
                        ["xclip", "-selection", "clipboard"],
                        input=content.encode("utf-8"),
                        check=True,
                    )
                    return {"success": True, "backend": "xclip"}
                except Exception:
                    subprocess.run(
                        ["xsel", "-ib"],
                        input=content.encode("utf-8"),
                        check=True,
                    )
                    return {"success": True, "backend": "xsel"}
        except Exception as e:
            last_err = str(e)

        return {"success": False, "error": last_err or "Failed to write to clipboard with available backends."}

    def _create_temp_file_from_image(self, image: Image.Image) -> Optional[str]:
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
            fd, path = tempfile.mkstemp(prefix="clipboard_", suffix=".png")
            os.close(fd)
            image.save(path, format="PNG")
            self._temp_files.append(path)
            return path
        except Exception:
            try:
                if 'path' in locals() and os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
            return None

    def _read_text(self) -> Optional[str]:
        # Try pyperclip
        try:
            if pyperclip is not None:
                text = pyperclip.paste()
                if isinstance(text, str):
                    return text
        except Exception:
            pass

        # Try tkinter
        try:
            if tk is not None:
                root = tk.Tk()
                try:
                    root.withdraw()
                    text = root.clipboard_get()
                    return text  # type: ignore
                finally:
                    try:
                        root.destroy()
                    except Exception:
                        pass
        except Exception:
            pass

        # Try OS commands
        try:
            if self._platform == "darwin":
                proc = subprocess.run(
                    ["pbpaste"], check=True, capture_output=True)
                return proc.stdout.decode("utf-8")
            elif self._platform.startswith("win"):
                # Prefer PowerShell if available
                try:
                    proc = subprocess.run(
                        ["powershell", "-NoProfile",
                            "-Command", "Get-Clipboard -Raw"],
                        check=True,
                        capture_output=True,
                    )
                    return proc.stdout.decode("utf-8", errors="ignore")
                except Exception:
                    pass
            else:
                # Linux: xclip, xsel
                try:
                    proc = subprocess.run(
                        ["xclip", "-selection", "clipboard", "-o"],
                        check=True,
                        capture_output=True,
                    )
                    return proc.stdout.decode("utf-8", errors="ignore")
                except Exception:
                    proc = subprocess.run(
                        ["xsel", "-ob"],
                        check=True,
                        capture_output=True,
                    )
                    return proc.stdout.decode("utf-8", errors="ignore")
        except Exception:
            pass

        return None

    def _read_image_or_files(self) -> Dict[str, Any]:
        if ImageGrab is None:
            return {"success": True, "type": "unsupported"}
        try:
            data = ImageGrab.grabclipboard()  # type: ignore[attr-defined]
            if data is None:
                return {"success": True, "type": "none"}
            if Image is not None and isinstance(data, Image.Image):
                return {"success": True, "type": "image", "image": data}
            if isinstance(data, (list, tuple)):
                files = [str(p) for p in data if isinstance(
                    p, (str, os.PathLike)) and os.path.exists(p)]
                if files:
                    return {"success": True, "type": "files", "files": files}
            return {"success": True, "type": "unknown"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def read(self) -> Dict[str, Any]:
        '''
        Read content from the clipboard and automatically determine the content type.
        Returns:
            Dict containing the clipboard content or error information
        '''
        # First, try to detect image or files via ImageGrab if available
        meta = self._read_image_or_files()
        if not meta.get("success", False):
            return meta

        mtype = meta.get("type")
        if mtype in ("image", "files"):
            return meta
        # If not image/files, try text
        text = self._read_text()
        if text is not None:
            return {"success": True, "type": "text", "content": text}
        # If everything fails
        return {"success": True, "type": "empty"}

    def read_and_process_paste(self) -> Dict[str, Any]:
        '''
        Read clipboard content and if it's an image or binary file, create a temporary file
        and return a file command that can be processed.
        Returns:
            Dict containing either processed file command or regular text content
        '''
        result = self.read()
        if not result.get("success", False):
            return result

        ctype = result.get("type")
        if ctype == "image":
            image = result.get("image")
            if Image is None or image is None:
                return {"success": False, "error": "PIL.Image unavailable or image missing."}
            temp_path = self._create_temp_file_from_image(image)
            if not temp_path:
                return {"success": False, "error": "Failed to create temporary file for image."}
            return {"success": True, "type": "file", "file_path": temp_path, "command": f"file:{temp_path}"}

        if ctype == "files":
            files = result.get("files", [])
            commands = [f"file:{p}" for p in files]
            first = files[0] if files else None
            return {
                "success": True,
                "type": "files",
                "files": files,
                "commands": commands,
                "file_path": first,
                "command": f"file:{first}" if first else None,
            }

        if ctype == "text":
            return {"success": True, "type": "text", "content": result.get("content", "")}

        return {"success": True, "type": ctype}

    def cleanup_temp_files(self):
        '''Clean up any temporary files created by this service.'''
        remaining: List[str] = []
        for p in self._temp_files:
            try:
                if os.path.exists(p):
                    os.remove(p)
            except Exception:
                remaining.append(p)
        self._temp_files = remaining

    def write_text(self, content: str) -> Dict[str, Any]:
        '''
        Write content to the clipboard.
        Args:
            content: Content to write to clipboard
        Returns:
            Dict containing success status and any error information
        '''
        try:
            if pyperclip is not None:
                pyperclip.copy(content)
                return {"success": True, "backend": "pyperclip"}
        except Exception as e:
            last_err = str(e)
        else:
            last_err = ""

        try:
            if tk is not None:
                root = tk.Tk()
                try:
                    root.withdraw()
                    root.clipboard_clear()
                    root.clipboard_append(content)
                    root.update()
                    return {"success": True, "backend": "tkinter"}
                finally:
                    try:
                        root.destroy()
                    except Exception:
                        pass
        except Exception as e:
            last_err = str(e)

        try:
            if self._platform == "darwin":
                subprocess.run(
                    ["pbcopy"], input=content.encode("utf-8"), check=True)
                return {"success": True, "backend": "pbcopy"}
            elif self._platform.startswith("win"):
                subprocess.run("clip", input=content.encode(
                    "utf-16le"), check=True, shell=True)
                return {"success": True, "backend": "clip"}
            else:
                try:
                    subprocess.run(
                        ["xclip", "-selection", "clipboard"],
                        input=content.encode("utf-8"),
                        check=True,
                    )
                    return {"success": True, "backend": "xclip"}
                except Exception:
                    subprocess.run(
                        ["xsel", "-ib"],
                        input=content.encode("utf-8"),
                        check=True,
                    )
                    return {"success": True, "backend": "xsel"}
        except Exception as e:
            last_err = str(e)

        return {"success": False, "error": last_err or "Failed to write to clipboard with available backends."}

    def __del__(self):
        '''Cleanup temporary files when the service is destroyed.'''
        try:
            self.cleanup_temp_files()
        except Exception:
            pass
