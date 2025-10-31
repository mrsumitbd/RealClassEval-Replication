
from __future__ import annotations

import os
import struct
from pathlib import Path
from typing import Dict, Optional, Tuple


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
        self.rom_path: Optional[Path] = None
        self.rom_data: Optional[bytes] = None

        if rom_file_path:
            self.load_rom_file(rom_file_path)

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        '''
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        '''
        sysfs_path = Path(f"/sys/bus/pci/devices/{bdf}/rom")
        if not sysfs_path.is_file():
            return False, f"ROM file not found for {bdf}"

        try:
            rom_bytes = sysfs_path.read_bytes()
        except Exception as e:
            return False, f"Failed to read ROM: {e}"

        self.output_dir.mkdir(parents=True, exist_ok=True)
        rom_file = self.output_dir / \
            f"{bdf.replace(':', '_').replace('.', '_')}_rom.bin"
        try:
            rom_file.write_bytes(rom_bytes)
        except Exception as e:
            return False, f"Failed to write ROM: {e}"

        self.rom_path = rom_file
        self.rom_data = rom_bytes
        return True, str(rom_file)

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        '''
        Load ROM data from a file
        '''
        path = Path(file_path) if file_path else self.rom_path
        if not path or not path.is_file():
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
        if not self.rom_data:
            return False

        out_path = Path(
            output_path) if output_path else self.output_dir / "rom_init.hex"
        out_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with out_path.open("w") as f:
                # Write 32‑bit words in big‑endian hex
                for i in range(0, len(self.rom_data), 4):
                    chunk = self.rom_data[i:i+4]
                    # Pad to 4 bytes
                    if len(chunk) < 4:
                        chunk = chunk.ljust(4, b"\x00")
                    word = struct.unpack(">I", chunk)[0]
                    f.write(f"{word:08X}\n")
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
        if not self.rom_data:
            return info

        info["size_bytes"] = str(len(self.rom_data))
        info["rom_path"] = str(self.rom_path) if self.
