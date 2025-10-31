
from typing import Optional, Tuple, Dict
from pathlib import Path
import os
import subprocess


class OptionROMManager:
    '''Manager for Option-ROM extraction and handling'''

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        '''
        Initialize the Option-ROM manager
        Args:
            output_dir: Path to directory for storing extracted ROM
            rom_file_path: Path to an existing ROM file to use instead of extraction
        '''
        self.output_dir = output_dir or Path('.')
        self.rom_file_path = rom_file_path
        self.rom_data = None

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        '''
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        '''
        rom_path = self.output_dir / f"rom_{bdf}.bin"
        try:
            subprocess.run(['setpci', '-s', bdf, 'ROM_BASE_ADDR'], check=True)
            subprocess.run(
                ['dd', 'if=/dev/mem', f'of={rom_path}', 'bs=1k', 'skip=128', 'count=128'], check=True)
            self.rom_file_path = str(rom_path)
            return True, str(rom_path)
        except subprocess.CalledProcessError:
            return False, ''

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        '''
        Load ROM data from a file
        Args:
            file_path: Path to ROM file (uses self.rom_file_path if None)
        Returns:
            True if ROM was loaded successfully
        '''
        file_path = file_path or self.rom_file_path
        if not file_path or not os.path.exists(file_path):
            return False
        with open(file_path, 'rb') as f:
            self.rom_data = f.read()
        return True

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
        output_path = output_path or self.output_dir / 'rom_init.hex'
        with open(output_path, 'w') as f:
            for i in range(0, len(self.rom_data), 4):
                word = self.rom_data[i:i+4]
                f.write(f"{word.hex()}\n")
        return True

    def get_rom_info(self) -> Dict[str, str]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        if self.rom_data is None:
            return {}
        return {
            'size': f"{len(self.rom_data)} bytes",
            'file_path': self.rom_file_path or 'Not specified'
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
        if not use_existing_rom or not self.load_rom_file():
            success, rom_path = self.extract_rom_linux(bdf)
            if not success:
                return {'error': 'Failed to extract ROM'}
            self.load_rom_file(rom_path)
        self.save_rom_hex()
        return self.get_rom_info()
