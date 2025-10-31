
from typing import Optional, Tuple, Dict
from pathlib import Path
import subprocess
import re


class OptionROMManager:

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        self.output_dir = output_dir if output_dir else Path('.')
        self.rom_file_path = rom_file_path
        self.rom_data = None
        self.rom_info = {}

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        try:
            command = f"setpci -s {bdf} 3e.b"
            output = subprocess.check_output(
                command, shell=True).decode().strip()
            rom_address = int(output, 16) * 0x1000
            command = f"dd if=/dev/mem of=rom.bin bs=1k skip={rom_address//1024} count=64"
            subprocess.check_output(command, shell=True)
            self.rom_file_path = 'rom.bin'
            return True, 'ROM extracted successfully'
        except subprocess.CalledProcessError as e:
            return False, f'Failed to extract ROM: {e}'

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        file_path = file_path if file_path else self.rom_file_path
        if not file_path:
            return False
        try:
            with open(file_path, 'rb') as f:
                self.rom_data = f.read()
            return True
        except Exception as e:
            return False

    def save_rom_hex(self, output_path: Optional[str] = None) -> bool:
        if not self.rom_data:
            return False
        output_path = output_path if output_path else str(
            self.output_dir / 'rom.hex')
        try:
            with open(output_path, 'w') as f:
                for i, byte in enumerate(self.rom_data):
                    f.write(f'{byte:02x}\n')
            return True
        except Exception as e:
            return False

    def get_rom_info(self) -> Dict[str, str]:
        if not self.rom_data:
            return {}
        # Assuming the ROM data is in the standard PCI expansion ROM format
        # https://wiki.osdev.org/PCI_Expansion_ROM
        signature = self.rom_data[:2].decode()
        if signature != '55aa':
            return {}
        self.rom_info['signature'] = signature
        self.rom_info['size'] = str(self.rom_data[2] * 512)
        return self.rom_info

    def setup_option_rom(self, bdf: str, use_existing_rom: bool = False) -> Dict[str, str]:
        if not use_existing_rom:
            success, message = self.extract_rom_linux(bdf)
            if not success:
                return {'error': message}
        if not self.load_rom_file():
            return {'error': 'Failed to load ROM file'}
        self.save_rom_hex()
        return self.get_rom_info()
