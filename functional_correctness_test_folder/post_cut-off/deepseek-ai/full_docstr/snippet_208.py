
from pathlib import Path
from typing import Optional, Tuple, Dict
import os
import subprocess
import struct


class OptionROMManager:
    '''Manager for Option-ROM extraction and handling'''

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        '''
        Initialize the Option-ROM manager
        Args:
            output_dir: Path to directory for storing extracted ROM
            rom_file_path: Path to an existing ROM file to use instead of extraction
        '''
        self.output_dir = output_dir or Path.cwd()
        self.rom_file_path = rom_file_path
        self.rom_data = None
        self.rom_info = {}

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        '''
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        '''
        rom_path = self.output_dir / f"rom_{bdf.replace(':', '_')}.bin"
        try:
            with open(f"/sys/bus/pci/devices/{bdf}/rom", "rb+") as rom_file:
                rom_file.write(b'1')
                rom_file.seek(0)
                self.rom_data = rom_file.read()
                rom_file.write(b'0')
            with open(rom_path, "wb") as f:
                f.write(self.rom_data)
            return True, str(rom_path)
        except Exception as e:
            return False, str(e)

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
        if not self.rom_data:
            return False
        path = output_path or str(self.output_dir / "rom_init.hex")
        try:
            with open(path, "w") as f:
                for i in range(0, len(self.rom_data), 4):
                    chunk = self.rom_data[i:i+4]
                    if len(chunk) < 4:
                        chunk += b'\x00' * (4 - len(chunk))
                    word = struct.unpack("<I", chunk)[0]
                    f.write(f"{word:08x}\n")
            return True
        except Exception:
            return False

    def get_rom_info(self) -> Dict[str, str]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        if not self.rom_data:
            return {}
        info = {}
        if len(self.rom_data) >= 24:
            signature = self.rom_data[:2]
            if signature == b'\x55\xAA':
                info['signature'] = '0x55AA (Valid)'
                info['size'] = f"{len(self.rom_data)} bytes"
                info['last_byte'] = f"0x{self.rom_data[-1]:02X}"
            else:
                info['signature'] = 'Invalid'
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
            if not self.load_rom_file():
                return {'error': 'Failed to load existing ROM file'}
        else:
            success, _ = self.extract_rom_linux(bdf)
            if not success:
                return {'error': 'Failed to extract ROM'}
        if not self.save_rom_hex():
            return {'error': 'Failed to save ROM hex file'}
        return self.get_rom_info()
