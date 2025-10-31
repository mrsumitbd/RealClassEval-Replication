
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
        if output_dir is not None:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path.cwd() / "option_rom_output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rom_file_path = rom_file_path
        self.rom_data = None
        self.rom_size = 0
        self.rom_loaded = False

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
            enable_path = f"/sys/bus/pci/devices/{bdf}/rom"
            with open(enable_path, "rb+") as rom_file:
                # Write "1" to enable
                rom_file.write(b"1")
            # Read ROM
            with open(rom_sysfs_path, "rb") as rom_file:
                rom_data = rom_file.read()
            # Disable ROM
            with open(enable_path, "rb+") as rom_file:
                rom_file.write(b"0")
            # Save to file
            with open(rom_out_path, "wb") as out_file:
                out_file.write(rom_data)
            self.rom_file_path = str(rom_out_path)
            return True, str(rom_out_path)
        except Exception as e:
            return False, ""

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        '''
        Load ROM data from a file
        Args:
            file_path: Path to ROM file (uses self.rom_file_path if None)
        Returns:
            True if ROM was loaded successfully
        '''
        path = file_path or self.rom_file_path
        if not path:
            return False
        try:
            with open(path, "rb") as f:
                self.rom_data = f.read()
            self.rom_size = len(self.rom_data)
            self.rom_loaded = True
            return True
        except Exception:
            self.rom_data = None
            self.rom_size = 0
            self.rom_loaded = False
            return False

    def save_rom_hex(self, output_path: Optional[str] = None) -> bool:
        '''
        Save ROM data in a format suitable for SystemVerilog $readmemh
        Args:
            output_path: Path to save the hex file (default: output_dir/rom_init.hex)
        Returns:
            True if data was saved successfully
        '''
        if not self.rom_loaded or self.rom_data is None:
            return False
        if output_path is None:
            output_path = self.output_dir / "rom_init.hex"
        else:
            output_path = Path(output_path)
        try:
            with open(output_path, "w") as f:
                for i in range(0, len(self.rom_data), 16):
                    chunk = self.rom_data[i:i+16]
                    hex_line = ''.join(f"{b:02x}" for b in chunk)
                    f.write(hex_line + "\n")
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
        info['rom_loaded'] = str(self.rom_loaded)
        info['rom_size'] = str(self.rom_size)
        if self.rom_loaded and self.rom_data:
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
        else:
            success, rom_path = self.extract_rom_linux(bdf)
            if not success:
                return {'error': 'ROM extraction failed'}
            loaded = self.load_rom_file(rom_path)
        if not loaded:
            return {'error': 'ROM loading failed'}
        saved = self.save_rom_hex()
        if not saved:
            return {'error': 'ROM hex save failed'}
        return self.get_rom_info()
