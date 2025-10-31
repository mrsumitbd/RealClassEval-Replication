
import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple, Dict


class OptionROMManager:
    '''Manager for Option-ROM extraction and handling'''

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        '''
        Initialize the Option-ROM manager
        Args:
            output_dir: Path to directory for storing extracted ROM
            rom_file_path: Path to an existing ROM file to use instead of extraction
        '''
        self.output_dir = output_dir if output_dir else Path('./rom_output')
        self.rom_file_path = rom_file_path
        self.rom_data = bytearray()
        self.rom_info = {}

        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)

        if self.rom_file_path:
            self.load_rom_file(self.rom_file_path)

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        '''
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        '''
        rom_path = self.output_dir / f'{bdf}.rom'
        try:
            with open(f'/sys/bus/pci/devices/{bdf}/rom', 'rb') as src, open(rom_path, 'wb') as dst:
                dst.write(src.read())
            return True, str(rom_path)
        except Exception as e:
            print(f'Error extracting ROM: {e}')
            return False, ''

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        '''
        Load ROM data from a file
        Args:
            file_path: Path to the ROM file (default: self.rom_file_path)
        Returns:
            True if data was loaded successfully
        '''
        file_path = file_path if file_path else self.rom_file_path
        if not file_path:
            return False

        try:
            with open(file_path, 'rb') as f:
                self.rom_data = bytearray(f.read())
            self.rom_file_path = file_path
            return True
        except Exception as e:
            print(f'Error loading ROM file: {e}')
            return False

    def save_rom_hex(self, output_path: Optional[str] = None) -> bool:
        '''
        Save ROM data in a format suitable for SystemVerilog $readmemh
        Args:
            output_path: Path to save the hex file (default: output_dir/rom_init.hex)
        Returns:
            True if data was saved successfully
        '''
        output_path = output_path if output_path else str(
            self.output_dir / 'rom_init.hex')
        try:
            with open(output_path, 'w') as f:
                for byte in self.rom_data:
                    f.write(f'{byte:02x}\n')
            return True
        except Exception as e:
            print(f'Error saving ROM hex file: {e}')
            return False

    def get_rom_info(self) -> Dict[str, str]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        # Assuming a simple ROM info extraction for demonstration purposes
        self.rom_info['size'] = f'{len(self.rom_data)} bytes'
        self.rom_info['file_path'] = self.rom_file_path
        return self.rom_info

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
            if self.load_rom_file():
                self.save_rom_hex()
                return self.get_rom_info()

        success, rom_path = self.extract_rom_linux(bdf)
        if success:
            self.load_rom_file(rom_path)
            self.save_rom_hex()
            return self.get_rom_info()
        else:
            return {}
