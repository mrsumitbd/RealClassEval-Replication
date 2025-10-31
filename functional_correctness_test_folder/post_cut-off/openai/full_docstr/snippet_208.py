
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
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rom_file_path = Path(rom_file_path) if rom_file_path else None
        self.rom_data: Optional[bytes] = None

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
            # Enable ROM if not already enabled
            with open(sys_path, "rb") as f:
                data = f.read()
            rom_path = self.output_dir / f"{bdf.replace(':', '_')}_rom.bin"
            with open(rom_path, "wb") as f:
                f.write(data)
            self.rom_data = data
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
        out_path = Path(
            output_path) if output_path else self.output_dir / "rom_init.hex"
        try:
            with open(out_path, "w") as f:
                # Write 16-bit words per line
                for i in range(0, len(self.rom_data), 2):
                    word = self.rom_data[i:i+2]
                    if len(word) < 2:
                        word = word.ljust(2, b'\x00')
                    f.write(f"{int.from_bytes(word, 'big'):04X}\n")
            return True
        except Exception:
            return False

    def get_rom_info(self) -> Dict[str, str]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        info: Dict[str, str] = {}
        if self.rom_data is None:
            return info
        info["size_bytes"] = str(len(self.rom_data))
        # Signature check (first two bytes)
        if len(self.rom_data) >= 2:
            sig = int.from_bytes(self.rom_data[:2], "big")
            info["signature"] = f"0x{sig:04X}"
        else:
            info["signature"] = "N/A"
        # Vendor ID (bytes 0x0E-0x0F in PCI header)
        if len(self.rom_data) >= 0x10:
            vendor_id = int.from_bytes(self.rom_data[0x0E:0x10], "little")
            info["vendor_id"] = f"0x{vendor_id:04X}"
        else:
            info["vendor_id"] = "N/A"
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
            loaded = self.load_rom_file()
            if not loaded:
                # fallback to extraction
                success, _ = self.extract_rom_linux(bdf)
                if not success:
                    return {}
        else:
            success, _ = self.extract_rom_linux(bdf)
            if not success:
                return {}

        self.save_rom_hex()
        return self.get_rom_info()
