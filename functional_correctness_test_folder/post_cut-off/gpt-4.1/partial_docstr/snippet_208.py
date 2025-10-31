
from typing import Optional, Tuple, Dict
from pathlib import Path
import os
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
        if output_dir is None:
            self.output_dir = Path.cwd() / "option_rom"
        else:
            self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rom_file_path = rom_file_path
        self.rom_data = None
        self.rom_size = 0
        self.rom_bdf = None

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        '''
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        '''
        rom_sysfs_path = f"/sys/bus/pci/devices/{bdf}/rom"
        rom_out_path = self.output_dir / \
            f"{bdf.replace(':', '_').replace('.', '_')}_option.rom"
        try:
            # Enable ROM
            with open(rom_sysfs_path, "rb+") as rom_file:
                rom_file.write(b"1")
            # Read ROM
            with open(rom_sysfs_path, "rb") as rom_file:
                rom_data = rom_file.read()
            # Disable ROM
            with open(rom_sysfs_path, "wb") as rom_file:
                rom_file.write(b"0")
            # Save ROM
            with open(rom_out_path, "wb") as out_file:
                out_file.write(rom_data)
            self.rom_file_path = str(rom_out_path)
            self.rom_data = rom_data
            self.rom_size = len(rom_data)
            self.rom_bdf = bdf
            return True, str(rom_out_path)
        except Exception as e:
            return False, str(e)

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        if file_path is not None:
            self.rom_file_path = file_path
        if self.rom_file_path is None:
            return False
        try:
            with open(self.rom_file_path, "rb") as f:
                self.rom_data = f.read()
            self.rom_size = len(self.rom_data)
            return True
        except Exception:
            self.rom_data = None
            self.rom_size = 0
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
        if output_path is None:
            output_path = self.output_dir / "rom_init.hex"
        else:
            output_path = Path(output_path)
        try:
            with open(output_path, "w") as f:
                for i in range(0, len(self.rom_data), 4):
                    word = self.rom_data[i:i+4]
                    hexstr = word.hex()
                    # Pad to 8 hex digits (32 bits)
                    hexstr = hexstr.ljust(8, '0')
                    f.write(hexstr + "\n")
            return True
        except Exception:
            return False

    def get_rom_info(self) -> Dict[str, str]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        info = {}
        info['rom_file_path'] = str(
            self.rom_file_path) if self.rom_file_path else ""
        info['rom_size'] = str(self.rom_size)
        info['rom_bdf'] = self.rom_bdf if self.rom_bdf else ""
        if self.rom_data:
            info['rom_crc32'] = f"{binascii.crc32(self.rom_data) & 0xffffffff:08x}"
        else:
            info['rom_crc32'] = ""
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
        if use_existing_rom and self.rom_file_path:
            loaded = self.load_rom_file()
            if not loaded:
                return {"error": "Failed to load existing ROM file"}
        else:
            success, rom_path = self.extract_rom_linux(bdf)
            if not success:
                return {"error": f"ROM extraction failed: {rom_path}"}
        if not self.save_rom_hex():
            return {"error": "Failed to save ROM hex file"}
        return self.get_rom_info()
