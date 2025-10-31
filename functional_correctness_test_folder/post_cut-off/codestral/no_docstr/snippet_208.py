
from pathlib import Path
from typing import Optional, Tuple, Dict
import subprocess
import os


class OptionROMManager:

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        self.output_dir = output_dir if output_dir is not None else Path.cwd()
        self.rom_file_path = rom_file_path
        self.rom_data = None

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        try:
            result = subprocess.run(
                ['setpci', '-s', bdf, 'CAP_EXP+0x70.l'], capture_output=True, text=True, check=True)
            rom_address = int(result.stdout.strip(), 16)
            rom_size = 1 << ((rom_address >> 16) & 0xF)
            rom_address &= 0xFFFF

            with open(f'/sys/bus/pci/devices/{bdf}/resource0', 'rb') as f:
                f.seek(rom_address)
                self.rom_data = f.read(rom_size)

            return True, "ROM extracted successfully"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to extract ROM: {e.stderr}"
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        if file_path is None:
            file_path = self.rom_file_path
        if file_path is None:
            return False

        try:
            with open(file_path, 'rb') as f:
                self.rom_data = f.read()
            return True
        except Exception:
            return False

    def save_rom_hex(self, output_path: Optional[str] = None) -> bool:
        if self.rom_data is None:
            return False

        if output_path is None:
            output_path = str(self.output_dir / 'option_rom.hex')

        try:
            with open(output_path, 'w') as f:
                for i, byte in enumerate(self.rom_data):
                    if i % 16 == 0:
                        f.write(f'\n{byte:02X} ')
                    else:
                        f.write(f'{byte:02X} ')
            return True
        except Exception:
            return False

    def get_rom_info(self) -> Dict[str, str]:
        if self.rom_data is None:
            return {}

        info = {
            'size': f'{len(self.rom_data)} bytes',
            'header': ' '.join(f'{byte:02X}' for byte in self.rom_data[:16])
        }
        return info

    def setup_option_rom(self, bdf: str, use_existing_rom: bool = False) -> Dict[str, str]:
        if not use_existing_rom:
            success, message = self.extract_rom_linux(bdf)
            if not success:
                return {'status': 'failed', 'message': message}

        if self.rom_data is None:
            return {'status': 'failed', 'message': 'No ROM data available'}

        rom_info = self.get_rom_info()
        rom_info['status'] = 'success'
        rom_info['message'] = 'Option ROM setup completed successfully'
        return rom_info
