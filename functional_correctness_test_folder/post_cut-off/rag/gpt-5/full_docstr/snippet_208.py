from pathlib import Path
from typing import Optional, Tuple, Dict, List
import platform
import hashlib
import os
import re
import time


class OptionROMManager:
    '''Manager for Option-ROM extraction and handling'''

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        '''
        Initialize the Option-ROM manager
        Args:
            output_dir: Path to directory for storing extracted ROM
            rom_file_path: Path to an existing ROM file to use instead of extraction
        '''
        self.output_dir: Path = Path(output_dir) if output_dir else (
            Path.cwd() / 'option_rom')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rom_file_path: Optional[Path] = Path(
            rom_file_path) if rom_file_path else None
        self.rom_bytes: Optional[bytes] = None
        self.hex_file_path: Optional[Path] = None
        self.source: Optional[str] = None
        self.last_bdf: Optional[str] = None

    def _normalize_bdf(self, bdf: str) -> str:
        bdf = bdf.strip()
        if re.match(r'^[0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-7]$', bdf):
            return bdf.lower()
        if re.match(r'^[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-7]$', bdf):
            return f'0000:{bdf.lower()}'
        return bdf.lower()

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        '''
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        '''
        if platform.system().lower() != 'linux':
            return (False, '')
        bdf_norm = self._normalize_bdf(bdf)
        self.last_bdf = bdf_norm
        sysfs_dir = Path('/sys/bus/pci/devices') / bdf_norm
        rom_attr = sysfs_dir / 'rom'
        if not rom_attr.exists():
            return (False, '')
        enabled = False
        data: Optional[bytes] = None
        try:
            try:
                with open(rom_attr, 'wb', buffering=0) as f:
                    f.write(b'1')
                enabled = True
                time.sleep(0.01)
            except PermissionError:
                return (False, '')
            with open(rom_attr, 'rb') as f:
                data = f.read()
            if not data:
                return (False, '')
            file_name = f'{bdf_norm.replace(":", "_").replace(".", "_")}_option_rom.bin'
            dest = self.output_dir / file_name
            with open(dest, 'wb') as out:
                out.write(data)
            self.rom_bytes = data
            self.rom_file_path = dest
            self.source = 'extracted'
            return (True, str(dest))
        except Exception:
            return (False, '')
        finally:
            if enabled:
                try:
                    with open(rom_attr, 'wb', buffering=0) as f:
                        f.write(b'0')
                except Exception:
                    pass

    def _parse_hex_text(self, text: str) -> bytes:
        result: bytearray = bytearray()
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith('//') or line.startswith('#'):
                continue
            if line.startswith('@'):
                # Address directive for $readmemh; ignore and append sequentially
                continue
            tokens: List[str] = re.split(r'[\s,]+', line)
            for tok in tokens:
                if not tok:
                    continue
                tok = tok.lower()
                if tok.startswith('0x'):
                    tok = tok[2:]
                if not re.fullmatch(r'[0-9a-f]+', tok):
                    continue
                if len(tok) % 2 == 1:
                    tok = '0' + tok
                for i in range(0, len(tok), 2):
                    b = int(tok[i:i+2], 16)
                    result.append(b)
        return bytes(result)

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        '''
        Load ROM data from a file
        Args:
            file_path: Path to ROM file (uses self.rom_file_path if None)
        Returns:
            True if ROM was loaded successfully
        '''
        path = Path(file_path) if file_path else (
            self.rom_file_path if self.rom_file_path else None)
        if path is None:
            return False
        if not path.exists() or not path.is_file():
            return False
        try:
            raw = path.read_bytes()
            if b'\x00' in raw or any(c < 9 for c in raw[:64]):
                data = raw
            else:
                try:
                    data = self._parse_hex_text(
                        raw.decode('utf-8', errors='ignore'))
                except Exception:
                    data = raw
            if not data:
                return False
            self.rom_bytes = data
            self.rom_file_path = path
            self.source = 'file'
            return True
        except Exception:
            return False

    def save_rom_hex(self, output_path: Optional[str] = None) -> bool:
        '''
        Save ROM data in a format suitable for SystemVerilog $readmemh
        Args:
            output_path: Path to save the hex file (default: output_dir/rom_init.hex)
        Returns:
            True if data was saved successfully
        '''
        if self.rom_bytes is None:
            return False
        out_path = Path(output_path) if output_path else (
            self.output_dir / 'rom_init.hex')
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, 'w', encoding='utf-8') as f:
                for b in self.rom_bytes:
                    f.write(f'{b:02x}\n')
            self.hex_file_path = out_path
            return True
        except Exception:
            return False

    def get_rom_info(self) -> Dict[str, str]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        info: Dict[str, str] = {}
        size = len(self.rom_bytes) if self.rom_bytes is not None else 0
        info['rom_file'] = str(
            self.rom_file_path) if self.rom_file_path else ''
        info['hex_file'] = str(
            self.hex_file_path) if self.hex_file_path else ''
        info['size_bytes'] = str(size)
        info['source'] = self.source or ''
        info['bdf'] = self.last_bdf or ''
        if self.rom_bytes:
            md5 = hashlib.md5(self.rom_bytes).hexdigest()
            sha256 = hashlib.sha256(self.rom_bytes).hexdigest()
            sig_ok = 'true' if size >= 2 and self.rom_bytes[0:2] == b'\x55\xaa' else 'false'
            info['md5'] = md5
            info['sha256'] = sha256
            info['signature_ok'] = sig_ok
        else:
            info['md5'] = ''
            info['sha256'] = ''
            info['signature_ok'] = 'false'
        return info

    def setup_option_rom(self, bdf: str, use_existing_rom: bool = False) -> Dict[str, str]:
        '''
        Complete setup process: extract ROM, save hex file, and return info
        Args:
            bdf: PCIe Bus:Device.Function
            use_existing_rom: Use existing ROM file if available
        Returns:
            Dictionary with ROM information
        '''
        success = False
        if use_existing_rom and self.rom_file_path and Path(self.rom_file_path).exists():
            success = self.load_rom_file()
        else:
            success, _ = self.extract_rom_linux(bdf)
            if not success and self.rom_file_path:
                success = self.load_rom_file()
        if success:
            self.save_rom_hex()
        info = self.get_rom_info()
        info['status'] = 'success' if success else 'failure'
        return info
