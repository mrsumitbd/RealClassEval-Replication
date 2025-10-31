import os
import sys
import hashlib
from pathlib import Path
from typing import Optional, Tuple, Dict


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
            output_dir) if output_dir is not None else Path.cwd() / "option_rom"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rom_file_path: Optional[Path] = Path(
            rom_file_path) if rom_file_path else None
        self.hex_file_path: Optional[Path] = None
        self.rom_data: Optional[bytes] = None
        self.last_bdf: Optional[str] = None

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        """
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        """
        if not sys.platform.startswith("linux"):
            return (False, "")

        device_path = Path("/sys/bus/pci/devices") / bdf
        rom_sysfs = device_path / "rom"
        if not rom_sysfs.exists():
            return (False, "")

        try:
            # Enable ROM access
            with open(rom_sysfs, "wb") as f:
                f.write(b"1")

            # Read ROM
            with open(rom_sysfs, "rb") as f:
                data = f.read()

            # Disable ROM access
            with open(rom_sysfs, "wb") as f:
                f.write(b"0")

        except PermissionError:
            return (False, "")
        except OSError:
            return (False, "")

        if not data:
            return (False, "")

        safe_bdf = bdf.replace(":", "_").replace(".", "_")
        out_path = self.output_dir / f"{safe_bdf}_option_rom.bin"
        try:
            with open(out_path, "wb") as f:
                f.write(data)
        except OSError:
            return (False, "")

        self.rom_data = data
        self.rom_file_path = out_path
        self.last_bdf = bdf
        return (True, str(out_path))

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        """
        Load ROM data from a file
        Args:
            file_path: Path to ROM file (uses self.rom_file_path if None)
        Returns:
            True if ROM was loaded successfully
        """
        path = Path(file_path) if file_path else self.rom_file_path
        if path is None:
            return False
        try:
            with open(path, "rb") as f:
                data = f.read()
        except OSError:
            return False

        if not data:
            return False

        self.rom_data = data
        self.rom_file_path = path
        return True

    def save_rom_hex(self, output_path: Optional[str] = None) -> bool:
        """
        Save ROM data in a format suitable for SystemVerilog $readmemh
        Args:
            output_path: Path to save the hex file (default: output_dir/rom_init.hex)
        Returns:
            True if data was saved successfully
        """
        if not self.rom_data:
            return False

        hex_path = Path(output_path) if output_path else (
            self.output_dir / "rom_init.hex")
        try:
            with open(hex_path, "w", encoding="utf-8") as f:
                for b in self.rom_data:
                    f.write(f"{b:02x}\n")
        except OSError:
            return False

        self.hex_file_path = hex_path
        return True

    def get_rom_info(self) -> Dict[str, str]:
        """
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        """
        size = len(self.rom_data) if self.rom_data else 0
        md5 = hashlib.md5(self.rom_data).hexdigest() if self.rom_data else ""
        sha1 = hashlib.sha1(self.rom_data).hexdigest() if self.rom_data else ""
        return {
            "bdf": self.last_bdf or "",
            "rom_file_path": str(self.rom_file_path) if self.rom_file_path else "",
            "hex_file_path": str(self.hex_file_path) if self.hex_file_path else "",
            "size_bytes": str(size),
            "md5": md5,
            "sha1": sha1,
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
        success = False

        if use_existing_rom and self.rom_file_path:
            success = self.load_rom_file(self.rom_file_path)

        if not success:
            success, _ = self.extract_rom_linux(bdf)
            if not success and self.rom_file_path:
                success = self.load_rom_file(self.rom_file_path)

        if success:
            self.save_rom_hex()

        return self.get_rom_info()
