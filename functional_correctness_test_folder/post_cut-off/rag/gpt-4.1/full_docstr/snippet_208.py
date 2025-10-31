import os
import binascii
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
        self.output_dir = Path(
            output_dir) if output_dir else Path.cwd() / "option_rom"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rom_file_path = rom_file_path
        self.rom_data = None
        self.rom_size = 0
        self.rom_hex_path = None

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        '''
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        '''
        rom_sysfs_path = f"/sys/bus/pci/devices/{bdf}/rom"
        output_rom_path = str(
            self.output_dir / f"{bdf.replace(':', '_').replace('.', '_')}_option.rom")
        try:
            # Enable ROM read
            with open(rom_sysfs_path, "rb+") as rom_file:
                # Write "1" to enable ROM
                with open(f"/sys/bus/pci/devices/{bdf}/rom", "wb") as enable_file:
                    enable_file.write(b"1")
                rom_file.seek(0)
                rom_data = rom_file.read()
                with open(output_rom_path, "wb") as out_file:
                    out_file.write(rom_data)
            # Disable ROM read
            with open(f"/sys/bus/pci/devices/{bdf}/rom", "wb") as disable_file:
                disable_file.write(b"0")
            self.rom_file_path = output_rom_path
            return True, output_rom_path
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
        if not path or not os.path.isfile(path):
            return False
        try:
            with open(path, "rb") as f:
                self.rom_data = f.read()
                self.rom_size = len(self.rom_data)
                self.rom_file_path = path
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
        hex_path = output_path or str(self.output_dir / "rom_init.hex")
        try:
            with open(hex_path, "w") as f:
                for i in range(0, len(self.rom_data), 16):
                    line = self.rom_data[i:i+16]
                    hex_line = ''.join(f"{b:02x}" for b in line)
                    f.write(hex_line + "\n")
            self.rom_hex_path = hex_path
            return True
        except Exception:
            return False

    def get_rom_info(self) -> Dict[str, str]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        info = {
            "rom_file_path": str(self.rom_file_path) if self.rom_file_path else "",
            "rom_size": str(self.rom_size),
            "rom_hex_path": str(self.rom_hex_path) if self.rom_hex_path else "",
            "output_dir": str(self.output_dir)
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
        if use_existing_rom and self.rom_file_path:
            loaded = self.load_rom_file(self.rom_file_path)
            if not loaded:
                return {"error": "Failed to load existing ROM file."}
        else:
            success, rom_path = self.extract_rom_linux(bdf)
            if not success:
                return {"error": f"ROM extraction failed: {rom_path}"}
            loaded = self.load_rom_file(rom_path)
            if not loaded:
                return {"error": "Failed to load extracted ROM file."}
        saved = self.save_rom_hex()
        if not saved:
            return {"error": "Failed to save ROM hex file."}
        return self.get_rom_info()
