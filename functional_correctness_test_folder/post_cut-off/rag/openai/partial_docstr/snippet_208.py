
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import os
import struct
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
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.rom_file_path = Path(rom_file_path) if rom_file_path else None
        self.rom_data: Optional[bytes] = None
        self.rom_path: Optional[Path] = None
        self.bdf: Optional[str] = None

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        '''
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        '''
        self.bdf = bdf
        sys_path = Path(f"/sys/bus/pci/devices/{bdf}/rom")
        if not sys_path.exists():
            return False, ""

        try:
            # Enable the device to allow ROM read
            enable_path = Path(f"/sys/bus/pci/devices/{bdf}/enable")
            if enable_path.exists():
                enable_path.write_text("1")
            # Read ROM
            rom_bytes = sys_path.read_bytes()
            # Disable the device again
            if enable_path.exists():
                enable_path.write_text("0")
        except Exception:
            return False, ""

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        rom_path = self.output_dir / \
            f"{bdf.replace(':', '_').replace('.', '_')}_rom.bin"
        try:
            rom_path.write_bytes(rom_bytes)
        except Exception:
            return False, ""

        self.rom_data = rom_bytes
        self.rom_path = rom_path
        return True, str(rom_path)

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
            self.rom_data = path.read_bytes()
            self.rom_path = path
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
            with out_path.open("w") as f:
                # Write 32-bit words (4 bytes) per line
                for i in range(0, len(self.rom_data), 4):
                    chunk = self.rom_data[i:i+4]
                    # Pad to 4 bytes if necessary
                    if len(chunk) < 4:
                        chunk = chunk.ljust(4, b"\x00")
                    word = struct.unpack(">I", chunk)[0]
                    f.write(f"{word:08X}\n")
            return True
        except Exception:
            return False

    def get_rom_info(self) -> Dict[str, Any]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        info: Dict[str, Any] = {}
        if self.rom_data:
            info["size_bytes"] = len(self.rom_data)
            info["size_words"] = (len(self.rom_data) + 3) // 4
            info["first_word"] = f"{struct.unpack('>I', self.rom_data[:4].ljust(4, b'\x00'))[0]:08X}"
            info["rom_path"] = str(self.rom_path) if self.rom_path else None
            info["bdf"] = self.bdf
        else:
            info["error"] = "No ROM data loaded"
        return info

    def setup_option_rom(self, bdf: str, use_existing_rom: bool = False) -> Dict[str, Any]:
        '''
        Complete setup process: extract ROM, save hex file, and return info
        Args:
            bdf: PCIe Bus:Device.Function
            use_existing_rom: Use existing ROM file if available
        Returns:
            Dictionary with ROM information
        '''
        # Try to load existing ROM if requested
        if use_existing_rom and self.rom_file_path and self.rom_file_path.exists():
            loaded = self.load_rom_file()
            if not loaded:
                # Fall back to extraction
                success, path = self.extract_rom_linux(bdf)
                if not success:
                    return {"error": "Failed to extract ROM"}
        else:
            success, path = self.extract_rom_linux(bdf)
            if not success:
                return {"error": "Failed to extract ROM"}

        # Save hex representation
        hex_saved = self.save_rom_hex()
        if not hex_saved:
            return {"error": "Failed to save ROM hex"}

        return self.get_rom_info()
