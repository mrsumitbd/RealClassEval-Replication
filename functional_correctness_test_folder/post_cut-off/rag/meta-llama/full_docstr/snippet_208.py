
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple


class OptionROMManager:
    """Manager for Option-ROM extraction and handling"""

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        """
        Initialize the Option-ROM manager
        Args:
            output_dir: Path to directory for storing extracted ROM
            rom_file_path: Path to an existing ROM file to use instead of extraction
        """
        self.output_dir = output_dir or Path('.')
        self.rom_file_path = rom_file_path
        self.rom_data = None

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        """
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        """
        rom_path = self.output_dir / f'{bdf}.rom'
        try:
            subprocess.run(
                ['sudo', 'dd', f'if=/sys/bus/pci/devices/{bdf}/rom', f'of={rom_path}', 'bs=1k', 'count=64'], check=True)
            return True, str(rom_path)
        except subprocess.CalledProcessError as e:
            return False, str(e)

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        """
        Load ROM data from a file
        Args:
            file_path: Path to ROM file (uses self.rom_file_path if None)
        Returns:
            True if ROM was loaded successfully
        """
        file_path = file_path or self.rom_file_path
        if not file_path:
            return False
        try:
            with open(file_path, 'rb') as f:
                self.rom_data = f.read()
            return True
        except OSError as e:
            print(f"Error loading ROM file: {e}")
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
            return False
        output_path = output_path or str(self.output_dir / 'rom_init.hex')
        try:
            with open(output_path, 'w') as f:
                for i, byte in enumerate(self.rom_data):
                    f.write(f'{byte:02x}\n')
            return True
        except OSError as e:
            print(f"Error saving ROM hex file: {e}")
            return False

    def get_rom_info(self) -> Dict[str, str]:
        """
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        """
        if not self.rom_data:
            return {}
        # Assuming the ROM data contains a PCI expansion ROM header
        # https://wiki.osdev.org/PCI_EXPANSION_ROM
        pci_rom_header = self.rom_data[:0x20]
        info = {
            'signature': pci_rom_header[:2].hex(),
            'pci_header_offset': int.from_bytes(pci_rom_header[0x18:0x1a], 'little'),
        }
        return info

    def setup_option_rom(self, bdf: str, use_existing_rom: bool = False) -> Dict[str, str]:
        """
        Complete setup process: extract ROM, save hex file, and return info
        Args:
            bdf: PCIe Bus:Device.Function
            use_existing_rom: Use existing ROM file if available
        Returns:
            Dictionary with ROM information
        """
        if use_existing_rom and self.rom_file_path:
            if self.load_rom_file():
                self.save_rom_hex()
                return self.get_rom_info()
        success, rom_path = self.extract_rom_linux(bdf)
        if success:
            self.rom_file_path = rom_path
            if self.load_rom_file():
                self.save_rom_hex()
                return self.get_rom_info()
        return {}
