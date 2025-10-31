
from typing import Optional, Tuple, Dict
from pathlib import Path
import os


class OptionROMManager:

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        self.output_dir = output_dir or Path('.')
        self.rom_file_path = rom_file_path
        self.rom_data = None

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        try:
            rom_path = f"/sys/bus/pci/devices/{bdf}/rom"
            with open(rom_path, 'rb') as f:
                self.rom_data = f.read()
            return True, "ROM extracted successfully"
        except Exception as e:
            return False, str(e)

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        try:
            file_path = file_path or self.rom_file_path
            if not file_path:
                raise ValueError("No file path provided")
            with open(file_path, 'rb') as f:
                self.rom_data = f.read()
            return True
        except Exception as e:
            print(f"Error loading ROM file: {e}")
            return False

    def save_rom_hex(self, output_path: Optional[str] = None) -> bool:
        try:
            output_path = output_path or self.output_dir / "rom.hex"
            with open(output_path, 'w') as f:
                f.write(self.rom_data.hex())
            return True
        except Exception as e:
            print(f"Error saving ROM to hex: {e}")
            return False

    def get_rom_info(self) -> Dict[str, str]:
        if not self.rom_data:
            return {"error": "No ROM data loaded"}
        return {
            "size": f"{len(self.rom_data)} bytes",
            "checksum": f"{sum(self.rom_data) & 0xFF:02X}"
        }

    def setup_option_rom(self, bdf: str, use_existing_rom: bool = False) -> Dict[str, str]:
        if not use_existing_rom:
            success, message = self.extract_rom_linux(bdf)
            if not success:
                return {"error": message}
        else:
            if not self.rom_data:
                return {"error": "No existing ROM data to use"}

        output_path = self.output_dir / f"{bdf}_rom.hex"
        if self.save_rom_hex(output_path):
            return {"status": "success", "output_path": str(output_path)}
        else:
            return {"error": "Failed to save ROM hex"}
