
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
        self.output_dir = output_dir if output_dir else Path.cwd()
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
        rom_path = self.output_dir / f"{bdf.replace(':', '_')}_rom.bin"
        try:
            subprocess.run(["setpci", "-s", bdf, "CAP_EXP+0x34.l=4"],
                           check=True, capture_output=True)
            subprocess.run(["setpci", "-s", bdf, "30.l=0x00000001"],
                           check=True, capture_output=True)
            subprocess.run(["lspci", "-s", bdf, "-xxx"],
                           check=True, capture_output=True, text=True)
            subprocess.run(
                ["dd", f"if=/sys/bus/pci/devices/{bdf}/rom", f"of={rom_path}"], check=True, capture_output=True)
            self.rom_file_path = str(rom_path)
            return True, str(rom_path)
        except subprocess.CalledProcessError as e:
            return False, str(e)

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
                self.rom_data = f.read()
            return True
        except IOError:
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
        output_path = output_path if output_path else str(
            self.output_dir / "rom_init.hex")
        try:
            with open(output_path, 'w') as f:
                for i in range(0, len(self.rom_data), 4):
                    chunk = self.rom_data[i:i+4]
                    hex_str = ''.join(
                        f"{byte:02x}" for byte in reversed(chunk))
                    f.write(f"{hex_str}\n")
            return True
        except IOError:
            return False

    def get_rom_info(self) -> Dict[str, str]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        if not self.rom_data:
            return {}
        rom_info = {
            "file_path": self.rom_file_path,
            "size": f"{len(self.rom_data)} bytes",
            "first_16_bytes": ' '.join(f"{byte:02x}" for byte in self.rom_data[:16])
        }
        return rom_info

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
            self.load_rom_file()
        else:
            success, rom_path = self.extract_rom_linux(bdf)
            if not success:
                return {}
            self.load_rom_file(rom_path)
        self.save_rom_hex()
        return self.get_rom_info()
