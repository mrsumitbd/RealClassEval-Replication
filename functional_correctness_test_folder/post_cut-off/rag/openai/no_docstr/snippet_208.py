
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple


class OptionROMManager:
    '''Manager for Option-ROM extraction and handling'''

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        '''
        Initialize the Option-ROM manager
        Args:
            output_dir: Path to directory for storing extracted ROM
            rom_file_path: Path to an existing ROM file to use instead of extraction
        '''
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.rom_file_path = Path(rom_file_path) if rom_file_path else None
        self.rom_data: Optional[bytes] = None
        self.rom_path: Optional[Path] = None

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        '''
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        '''
        sys_path = Path(f"/sys/bus/pci/devices/{bdf}/rom")
        if not sys_path.exists():
            return False, ""
        try:
            with open(sys_path, "rb") as f:
                data = f.read()
            if not data:
                return False, ""
            self.output_dir.mkdir(parents=True, exist_ok=True)
            rom_name = f"{bdf.replace(':', '_').replace('.', '_')}.rom"
            rom_path = self.output_dir / rom_name
            with open(rom_path, "wb") as f:
                f.write(data)
            self.rom_data = data
            self.rom_path = rom_path
            return True, str(rom_path)
        except Exception:
            return False, ""

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        '''
        Load ROM data from a file
        Args:
            file_path: Path to ROM file (uses self.rom_file_path if None)
        Returns:
            True if ROM was loaded successfully
        '''
        path = Path(file_path) if file_path else self.rom_file_path
        if not path or not path.exists():
            return False
        try:
            with open(path, "rb") as f:
                self.rom_data = f.read()
            self.rom_path = path
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
        if self.rom_data is None:
            return False
        out_path = Path(output_path) if output_path else (
            self.output_dir / "rom_init.hex")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(out_path, "w") as f:
                for i in range(0, len(self.rom_data), 4):
                    word = self.rom_data[i:i+4]
                    if len(word) < 4:
                        word = word.ljust(4, b'\x00')
                    f.write(f"{int.from_bytes(word, 'big'):08X}\n")
            return True
        except Exception:
            return False

    def get_rom_info(self) -> Dict[str, str]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        if self.rom_data is None:
            return {}
        info: Dict[str, str] = {
            "size_bytes": str(len(self.rom_data)),
            "rom_path": str(self.rom_path) if self.rom_path else "",
            "hex_file": str(self.output_dir / "rom_init.hex") if (self.output_dir / "rom_init.hex").exists() else ""
        }
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
        if use_existing_rom and self.rom_file_path and self.rom_file_path.exists():
            loaded = self.load_rom_file(str(self.rom_file_path))
            if not loaded:
                raise RuntimeError("Failed to load existing ROM file")
        else:
            success, rom_path = self.extract_rom_linux(bdf)
            if not success:
                raise RuntimeError(f"Failed to extract ROM from {bdf}")
        saved = self.save_rom_hex()
        if not saved:
            raise RuntimeError("Failed to save ROM hex")
        return self.get_rom_info()
