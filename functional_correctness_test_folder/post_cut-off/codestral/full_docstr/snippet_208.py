
import os
from pathlib import Path
from typing import Optional, Tuple, Dict
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
        self.output_dir = output_dir if output_dir is not None else Path.cwd()
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
        rom_path = self.output_dir / f"{bdf.replace(':', '_')}.rom"
        try:
            subprocess.run(["setpci", "-s", bdf, "CAP_EXP+0x34.l=4"],
                           check=True, capture_output=True)
            subprocess.run(["setpci", "-s", bdf, "30.l=0x00000000"],
                           check=True, capture_output=True)
            subprocess.run(["lspci", "-s", bdf, "-xxx"],
                           check=True, stdout=open(rom_path, 'w'))
            return (True, str(rom_path))
        except subprocess.CalledProcessError as e:
            print(f"Error extracting ROM: {e}")
            return (False, "")

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        '''
        Load ROM data from a file
        Args:
            file_path: Path to ROM file (uses self.rom_file_path if None)
        Returns:
            True if ROM was loaded successfully
        '''
        path = Path(file_path) if file_path is not None else Path(
            self.rom_file_path)
        if not path.exists():
            return False
        with open(path, 'rb') as f:
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
        path = Path(
            output_path) if output_path is not None else self.output_dir / "rom_init.hex"
        with open(path, 'w') as f:
            for i in range(0, len(self.rom_data), 16):
                chunk = self.rom_data[i:i+16]
                hex_line = ' '.join(f"{byte:02x}" for byte in chunk)
                f.write(f"{hex_line}\n")
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
            "size": f"{len(self.rom_data)} bytes",
            "hex_size": f"{len(self.rom_data) * 2} hex digits"
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
        if use_existing_rom and self.rom_file_path is not None and self.load_rom_file():
            self.save_rom_hex()
            return self.get_rom_info()
        success, rom_path = self.extract_rom_linux(bdf)
        if not success:
            return {}
        self.rom_file_path = rom_path
        self.load_rom_file()
        self.save_rom_hex()
        return self.get_rom_info()
