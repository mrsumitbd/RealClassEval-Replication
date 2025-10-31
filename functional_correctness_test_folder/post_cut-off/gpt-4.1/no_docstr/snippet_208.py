
from typing import Optional, Tuple, Dict
from pathlib import Path
import subprocess
import binascii
import os


class OptionROMManager:

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.rom_file_path = rom_file_path
        self.rom_data = None
        self.rom_info = {}

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        rom_path = Path(f"/sys/bus/pci/devices/{bdf}/rom")
        if not rom_path.exists():
            return False, f"ROM path {rom_path} does not exist"
        try:
            # Enable ROM
            enable_path = rom_path.parent / "rom"
            with open(rom_path.parent / "rom", "wb") as f:
                f.write(b'1')
            with open(rom_path, "rb") as f:
                rom_data = f.read()
            with open(rom_path.parent / "rom", "wb") as f:
                f.write(b'0')
            self.rom_data = rom_data
            self.rom_file_path = str(
                self.output_dir / f"{bdf.replace(':', '_').replace('.', '_')}_option.rom")
            with open(self.rom_file_path, "wb") as f:
                f.write(rom_data)
            return True, self.rom_file_path
        except Exception as e:
            return False, str(e)

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        path = file_path or self.rom_file_path
        if not path or not os.path.isfile(path):
            return False
        try:
            with open(path, "rb") as f:
                self.rom_data = f.read()
            self.rom_file_path = path
            return True
        except Exception:
            return False

    def save_rom_hex(self, output_path: Optional[str] = None) -> bool:
        if self.rom_data is None:
            return False
        out_path = output_path or (str(self.output_dir / "option_rom.hex"))
        try:
            with open(out_path, "w") as f:
                hexstr = binascii.hexlify(self.rom_data).decode("ascii")
                for i in range(0, len(hexstr), 32):
                    f.write(hexstr[i:i+32] + "\n")
            return True
        except Exception:
            return False

    def get_rom_info(self) -> Dict[str, str]:
        info = {}
        if self.rom_data is None:
            return info
        # Option ROM header is 0x55 0xAA at offset 0
        if self.rom_data[:2] == b'\x55\xaa':
            info['signature'] = '0x55AA'
            # PCI Data Structure pointer at offset 0x18 (little endian 16-bit)
            if len(self.rom_data) >= 0x1A:
                pci_data_ptr = int.from_bytes(
                    self.rom_data[0x18:0x1A], 'little')
                info['pci_data_pointer'] = hex(pci_data_ptr)
                if len(self.rom_data) >= pci_data_ptr + 0x16:
                    # PCI Data Structure signature "PCIR"
                    if self.rom_data[pci_data_ptr:pci_data_ptr+4] == b'PCIR':
                        info['pcir_signature'] = 'PCIR'
                        vendor_id = int.from_bytes(
                            self.rom_data[pci_data_ptr+4:pci_data_ptr+6], 'little')
                        device_id = int.from_bytes(
                            self.rom_data[pci_data_ptr+6:pci_data_ptr+8], 'little')
                        info['vendor_id'] = hex(vendor_id)
                        info['device_id'] = hex(device_id)
                        rom_revision = self.rom_data[pci_data_ptr+14]
                        info['rom_revision'] = str(rom_revision)
        self.rom_info = info
        return info

    def setup_option_rom(self, bdf: str, use_existing_rom: bool = False) -> Dict[str, str]:
        result = {}
        if use_existing_rom and self.rom_file_path:
            loaded = self.load_rom_file(self.rom_file_path)
            result['load_rom_file'] = str(loaded)
            if not loaded:
                result['error'] = "Failed to load existing ROM file"
                return result
        else:
            success, msg = self.extract_rom_linux(bdf)
            result['extract_rom_linux'] = str(success)
            if not success:
                result['error'] = msg
                return result
        info = self.get_rom_info()
        result.update(info)
        return result
