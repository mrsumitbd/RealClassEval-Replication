from pathlib import Path
from typing import Optional, Tuple, Dict
import os
import sys
import hashlib
import binascii


class OptionROMManager:
    '''Manager for Option-ROM extraction and handling'''

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        '''
        Initialize the Option-ROM manager
        Args:
            output_dir: Path to directory for storing extracted ROM
            rom_file_path: Path to an existing ROM file to use instead of extraction
        '''
        self.output_dir: Path = Path(
            output_dir) if output_dir is not None else Path.cwd() / "option_rom_out"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.rom_file_path: Optional[str] = rom_file_path
        self.rom_data: Optional[bytes] = None
        self.hex_file_path: Optional[str] = None
        self.last_bdf: Optional[str] = None
        self.last_error: Optional[str] = None
        self.source: Optional[str] = None

        if rom_file_path:
            self.load_rom_file(rom_file_path)

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        '''
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        '''
        self.last_error = None
        self.last_bdf = bdf

        if not sys.platform.startswith("linux"):
            self.last_error = "Option-ROM extraction is only supported on Linux."
            return False, ""

        dev_path = Path("/sys/bus/pci/devices") / bdf
        rom_sysfs = dev_path / "rom"
        if not rom_sysfs.exists():
            self.last_error = f"ROM sysfs node not found: {rom_sysfs}"
            return False, ""

        rom_bytes = b""
        try:
            with open(rom_sysfs, "wb", buffering=0) as f:
                f.write(b"1")
            try:
                with open(rom_sysfs, "rb") as f:
                    rom_bytes = f.read()
            finally:
                try:
                    with open(rom_sysfs, "wb", buffering=0) as f:
                        f.write(b"0")
                except Exception:
                    pass
        except PermissionError:
            self.last_error = f"Permission denied accessing {rom_sysfs}. Try running as root."
            return False, ""
        except Exception as e:
            self.last_error = f"Failed to read ROM from {rom_sysfs}: {e}"
            return False, ""

        if not rom_bytes:
            self.last_error = "Extracted ROM is empty."
            return False, ""

        out_path = self.output_dir / "option_rom.bin"
        try:
            with open(out_path, "wb") as f:
                f.write(rom_bytes)
        except Exception as e:
            self.last_error = f"Failed to save ROM to {out_path}: {e}"
            return False, ""

        self.rom_data = rom_bytes
        self.rom_file_path = str(out_path)
        self.source = "extracted"
        return True, str(out_path)

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        '''
        Load ROM data from a file
        Args:
            file_path: Path to ROM file (uses self.rom_file_path if None)
        Returns:
            True if ROM was loaded successfully
        '''
        self.last_error = None
        path = file_path or self.rom_file_path
        if not path:
            self.last_error = "No ROM file path provided."
            return False

        p = Path(path)
        if not p.is_file():
            self.last_error = f"ROM file not found: {p}"
            return False

        try:
            data = p.read_bytes()
        except Exception as e:
            self.last_error = f"Failed to read ROM file {p}: {e}"
            return False

        if not data:
            self.last_error = "ROM file is empty."
            return False

        self.rom_data = data
        self.rom_file_path = str(p)
        if self.source is None:
            self.source = "file"
        return True

    def save_rom_hex(self, output_path: Optional[str] = None) -> bool:
        '''
        Save ROM data in a format suitable for SystemVerilog $readmemh
        Args:
            output_path: Path to save the hex file (default: output_dir/rom_init.hex)
        Returns:
            True if data was saved successfully
        '''
        self.last_error = None
        if self.rom_data is None:
            self.last_error = "No ROM data loaded."
            return False

        out_path = Path(output_path) if output_path else (
            self.output_dir / "rom_init.hex")

        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                for b in self.rom_data:
                    f.write(f"{b:02x}\n")
        except Exception as e:
            self.last_error = f"Failed to write hex file {out_path}: {e}"
            return False

        self.hex_file_path = str(out_path)
        return True

    def get_rom_info(self) -> Dict[str, str]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        size = len(self.rom_data) if self.rom_data is not None else 0
        sha256 = ""
        if self.rom_data is not None:
            sha256 = hashlib.sha256(self.rom_data).hexdigest()

        return {
            "bdf": self.last_bdf or "",
            "rom_file": self.rom_file_path or "",
            "hex_file": self.hex_file_path or "",
            "size_bytes": str(size),
            "sha256": sha256,
            "source": self.source or "",
            "output_dir": str(self.output_dir),
            "last_error": self.last_error or "",
        }

    def setup_option_rom(self, bdf: str, use_existing_rom: bool = False) -> Dict[str, str]:
        '''
        Complete setup process: extract ROM, save hex file, and return info
        Args:
            bdf: PCIe Bus:Device.Function
            use_existing_rom: Use existing ROM file if available
        Returns:
            Dictionary with ROM information
        '''
        self.last_bdf = bdf
        ok = False

        if use_existing_rom and self.rom_file_path:
            ok = self.load_rom_file(self.rom_file_path)
        else:
            ok, _ = self.extract_rom_linux(bdf)

        if ok:
            self.save_rom_hex()

        return self.get_rom_info()
