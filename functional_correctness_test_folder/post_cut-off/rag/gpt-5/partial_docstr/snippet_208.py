from pathlib import Path
from typing import Optional, Tuple, Dict
import hashlib
import sys
import os


class OptionROMManager:
    """Manager for Option-ROM extraction and handling"""

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        """
        Initialize the Option-ROM manager
        Args:
            output_dir: Path to directory for storing extracted ROM
            rom_file_path: Path to an existing ROM file to use instead of extraction
        """
        self.output_dir: Path = Path(
            output_dir) if output_dir else Path.cwd() / "option_rom"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rom_file_path: Optional[str] = rom_file_path
        self.hex_file_path: Optional[str] = None
        self.rom_data: bytes = b""
        self.rom_size: int = 0
        self.rom_sha256: str = ""
        self.bdf: str = ""

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        """
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        """
        if not sys.platform.startswith("linux"):
            return False, ""

        device_dir = Path("/sys/bus/pci/devices") / bdf
        rom_sysfs = device_dir / "rom"
        if not rom_sysfs.exists():
            return False, ""

        toggled = False
        data: bytes = b""
        try:
            with open(rom_sysfs, "wb") as f:
                f.write(b"1")
            toggled = True

            with open(rom_sysfs, "rb") as f:
                data = f.read()

            if not data:
                return False, ""

            safe_bdf = bdf.replace(":", "_").replace(".", "_")
            out_path = self.output_dir / f"{safe_bdf}.rom"
            with open(out_path, "wb") as f:
                f.write(data)

            self.rom_data = data
            self.rom_size = len(data)
            self.rom_sha256 = hashlib.sha256(data).hexdigest()
            self.rom_file_path = str(out_path)
            return True, str(out_path)
        except PermissionError:
            return False, ""
        except OSError:
            return False, ""
        finally:
            if toggled:
                try:
                    with open(rom_sysfs, "wb") as f:
                        f.write(b"0")
                except Exception:
                    pass

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        """
        Load ROM data from a file
        Args:
            file_path: Path to ROM file (uses self.rom_file_path if None)
        Returns:
            True if ROM was loaded successfully
        """
        path = Path(file_path) if file_path else (
            Path(self.rom_file_path) if self.rom_file_path else None)
        if not path:
            return False
        if not path.exists() or not path.is_file():
            return False
        try:
            data = path.read_bytes()
            self.rom_data = data
            self.rom_size = len(data)
            self.rom_sha256 = hashlib.sha256(data).hexdigest()
            self.rom_file_path = str(path)
            return True
        except OSError:
            return False

    def save_rom_hex(self, output_path: Optional[str] = None) -> bool:
        """
        Save ROM data in a format suitable for SystemVerilog $readmemh
        Args:
            output_path: Path to save the hex file (default: output_dir/rom_init.hex)
        Returns:
            True if data was saved successfully
        """
        if not self.rom_data:
            if not self.rom_file_path or not self.load_rom_file(self.rom_file_path):
                return False

        out = Path(output_path) if output_path else self.output_dir / \
            "rom_init.hex"
        try:
            lines = (f"{b:02x}" for b in self.rom_data)
            out.write_text("\n".join(lines))
            self.hex_file_path = str(out)
            return True
        except OSError:
            return False

    def get_rom_info(self) -> Dict[str, str]:
        """
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        """
        return {
            "bdf": self.bdf or "",
            "rom_path": self.rom_file_path or "",
            "hex_path": self.hex_file_path or "",
            "size_bytes": str(self.rom_size),
            "sha256": self.rom_sha256 or "",
            "platform": sys.platform,
        }

    def setup_option_rom(self, bdf: str, use_existing_rom: bool = False) -> Dict[str, str]:
        """
        Complete setup process: extract ROM, save hex file, and return info
        Args:
            bdf: PCIe Bus:Device.Function
            use_existing_rom: Use existing ROM file if available
        Returns:
            Dictionary with ROM information
        """
        self.bdf = bdf

        loaded = False
        if use_existing_rom and self.rom_file_path and Path(self.rom_file_path).exists():
            loaded = self.load_rom_file(self.rom_file_path)

        if not loaded:
            if sys.platform.startswith("linux"):
                ok, _ = self.extract_rom_linux(bdf)
                loaded = ok
            else:
                loaded = False

        if loaded:
            self.save_rom_hex()

        return self.get_rom_info()
