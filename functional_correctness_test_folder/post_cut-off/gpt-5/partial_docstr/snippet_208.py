from pathlib import Path
from typing import Optional, Tuple, Dict
import os
import hashlib
import errno


class OptionROMManager:
    '''Manager for Option-ROM extraction and handling'''

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        '''
        Initialize the Option-ROM manager
        Args:
            output_dir: Path to directory for storing extracted ROM
            rom_file_path: Path to an existing ROM file to use instead of extraction
        '''
        self.output_dir: Path = Path(
            output_dir) if output_dir else Path.cwd() / "option_rom"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rom_file_path: Optional[Path] = Path(
            rom_file_path) if rom_file_path else None
        self.rom_data: Optional[bytes] = None
        self.hex_file_path: Optional[Path] = None
        self.last_bdf: Optional[str] = None

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        '''
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        '''
        sysfs_dev = Path("/sys/bus/pci/devices") / bdf
        rom_node = sysfs_dev / "rom"

        if not rom_node.exists():
            return (False, "")

        # Enable ROM read
        try:
            with open(rom_node, "wb", buffering=0) as f:
                f.write(b"1")
        except PermissionError:
            return (False, "")
        except OSError:
            return (False, "")

        # Read ROM contents
        rom_bytes: Optional[bytes] = None
        try:
            with open(rom_node, "rb", buffering=0) as f:
                rom_bytes = f.read()
        except Exception:
            rom_bytes = None
        finally:
            # Disable ROM read
            try:
                with open(rom_node, "wb", buffering=0) as f:
                    f.write(b"0")
            except Exception:
                pass

        if not rom_bytes:
            return (False, "")

        # Save to file
        out_path = self.output_dir / \
            f"{bdf.replace(':', '_').replace('.', '_')}_option_rom.bin"
        try:
            with open(out_path, "wb") as f:
                f.write(rom_bytes)
        except Exception:
            return (False, "")

        self.rom_file_path = out_path
        self.rom_data = rom_bytes
        self.last_bdf = bdf
        return (True, str(out_path))

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        path = Path(file_path) if file_path else (
            self.rom_file_path if self.rom_file_path else None)
        if not path:
            return False
        try:
            data = path.read_bytes()
        except Exception:
            return False
        self.rom_file_path = path
        self.rom_data = data
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
            # Try to load from file if path is set
            if self.rom_file_path and self.rom_file_path.exists():
                try:
                    self.rom_data = self.rom_file_path.read_bytes()
                except Exception:
                    return False
            else:
                return False

        out_path = Path(output_path) if output_path else (
            self.output_dir / "rom_init.hex")
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            return False

        try:
            with open(out_path, "w", encoding="ascii") as f:
                # One byte per line, two hex digits, no 0x prefix
                for b in self.rom_data:
                    f.write(f"{b:02x}\n")
        except Exception:
            return False

        self.hex_file_path = out_path
        return True

    def get_rom_info(self) -> Dict[str, str]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        info: Dict[str, str] = {}
        data = self.rom_data

        if data is None:
            if self.rom_file_path and self.rom_file_path.exists():
                try:
                    data = self.rom_file_path.read_bytes()
                    self.rom_data = data
                except Exception:
                    data = None

        if self.rom_file_path:
            info["rom_file"] = str(self.rom_file_path)
        if self.hex_file_path:
            info["hex_file"] = str(self.hex_file_path)
        if self.last_bdf:
            info["bdf"] = self.last_bdf

        if not data:
            info["size_bytes"] = "0"
            info["sha256"] = ""
            info["valid_signature"] = "false"
            info["is_uefi"] = "unknown"
            info["code_type"] = "unknown"
            return info

        info["size_bytes"] = str(len(data))
        info["sha256"] = hashlib.sha256(data).hexdigest()

        valid = len(data) >= 2 and data[0] == 0x55 and data[1] == 0xAA
        info["valid_signature"] = "true" if valid else "false"

        # Parse PCI Data Structure to infer code type if possible
        code_type = "unknown"
        is_uefi = "unknown"

        try:
            if len(data) >= 0x1C and valid:
                # Offset to PCI Data Structure in ROM header at 0x18 (little endian)
                pcir_off = int.from_bytes(data[0x18:0x1A], "little")
                if pcir_off + 0x16 <= len(data):
                    # "PCIR" signature
                    if data[pcir_off:pcir_off + 4] == b"PCIR":
                        # Code type at offset 0x14 within PCIR structure
                        ct = data[pcir_off + 0x14]
                        # Known types: 0x00 x86, 0x01 Open Firmware, 0x02 HP PA-RISC, 0x03 EFI Image
                        code_type_map = {
                            0x00: "x86",
                            0x01: "OpenFirmware",
                            0x02: "HP-PA",
                            0x03: "UEFI",
                        }
                        code_type = code_type_map.get(ct, f"0x{ct:02x}")
                        is_uefi = "true" if ct == 0x03 else "false"
        except Exception:
            pass

        info["code_type"] = code_type
        info["is_uefi"] = is_uefi

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
        success = False

        if use_existing_rom and self.rom_file_path:
            success = self.load_rom_file(str(self.rom_file_path))

        if not success:
            ok, _path = self.extract_rom_linux(bdf)
            if not ok:
                return self.get_rom_info()
            success = True

        if success:
            self.save_rom_hex()

        return self.get_rom_info()
