from pathlib import Path
import shlex
import os
from typing import Dict, Optional, Tuple
import subprocess

class OptionROMManager:
    """Manager for Option-ROM extraction and handling"""

    def __init__(self, output_dir: Optional[Path]=None, rom_file_path: Optional[str]=None):
        """
        Initialize the Option-ROM manager

        Args:
            output_dir: Path to directory for storing extracted ROM
            rom_file_path: Path to an existing ROM file to use instead of extraction
        """
        if output_dir is None:
            self.output_dir = Path(__file__).parent.parent / 'output'
        else:
            self.output_dir = Path(output_dir)
        self.rom_file_path = rom_file_path
        self.rom_size = 0
        self.rom_data = None

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        """
        Extract Option-ROM from a PCI device on Linux

        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")

        Returns:
            Tuple of (success, rom_path)
        """
        try:
            import re
            bdf_pattern = re.compile('^[0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\\.[0-7]$')
            if not bdf_pattern.match(bdf):
                raise OptionROMExtractionError(f'Invalid BDF format: {bdf}')
            self.output_dir.mkdir(exist_ok=True, parents=True)
            rom_path = self.output_dir / 'donor.rom'
            device_path = f'/sys/bus/pci/devices/{bdf}'
            if not os.path.exists(device_path):
                rom_path = self.output_dir / 'donor.rom'
                if not rom_path.exists():
                    raise OptionROMExtractionError(f'PCI device not found: {bdf}')
            rom_sysfs_path = f'{device_path}/rom'
            if not os.path.exists(rom_sysfs_path):
                rom_path = self.output_dir / 'donor.rom'
                if not rom_path.exists():
                    raise OptionROMExtractionError(f'ROM file not available for device: {bdf}')
            logger.info(f'Enabling ROM access for {bdf}')
            try:
                with open(rom_sysfs_path, 'w') as f:
                    f.write('1')
            except (OSError, IOError) as e:
                try:
                    subprocess.run(['sh', '-c', f'echo 1 > {shlex.quote(str(rom_sysfs_path))}'], check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as subprocess_e:
                    raise OptionROMExtractionError(f'Subprocess fallback failed to enable ROM access: {subprocess_e}')
            try:
                logger.info(f'Extracting ROM from {bdf} to {rom_path}')
                subprocess.run(['dd', f'if={rom_sysfs_path}', f'of={rom_path}', 'bs=4K'], check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                raise OptionROMExtractionError(f'Failed to extract ROM: {e}')
            finally:
                try:
                    with open(rom_sysfs_path, 'w') as f:
                        f.write('0')
                except (OSError, IOError):
                    try:
                        subprocess.run(['sh', '-c', f'echo 0 > {shlex.quote(str(rom_sysfs_path))}'], check=True, capture_output=True, text=True)
                    except subprocess.CalledProcessError as e:
                        logger.warning(f'Failed to disable ROM access: {e}')
            if not rom_path.exists():
                raise OptionROMExtractionError('ROM extraction failed: file not created')
            file_size = rom_path.stat().st_size
            if file_size == 0:
                raise OptionROMExtractionError('ROM extraction failed: file is empty')
            with open(rom_path, 'rb') as f:
                self.rom_data = f.read()
            self.rom_file_path = str(rom_path)
            self.rom_size = file_size
            logger.info(f'Successfully extracted ROM ({self.rom_size} bytes)')
            return (True, str(rom_path))
        except Exception as e:
            logger.error(f'ROM extraction failed: {e}')
            return (False, '')

    def load_rom_file(self, file_path: Optional[str]=None) -> bool:
        """
        Load ROM data from a file

        Args:
            file_path: Path to ROM file (uses self.rom_file_path if None)

        Returns:
            True if ROM was loaded successfully
        """
        try:
            path = file_path or self.rom_file_path
            if not path:
                raise OptionROMError('No ROM file path specified')
            rom_path = Path(path)
            if not rom_path.exists():
                raise OptionROMError(f'ROM file not found: {rom_path}')
            with open(rom_path, 'rb') as f:
                self.rom_data = f.read()
            self.rom_size = len(self.rom_data)
            logger.info(f'Loaded ROM file: {rom_path} ({self.rom_size} bytes)')
            return True
        except Exception as e:
            logger.error(f'Failed to load ROM file: {e}')
            return False

    def save_rom_hex(self, output_path: Optional[str]=None) -> bool:
        """
        Save ROM data in a format suitable for SystemVerilog $readmemh

        Args:
            output_path: Path to save the hex file (default: output_dir/rom_init.hex)

        Returns:
            True if data was saved successfully
        """
        try:
            if self.rom_data is None:
                if not self.load_rom_file():
                    raise OptionROMError('No ROM data available')
            if not output_path:
                output_path = str(self.output_dir / 'rom_init.hex')
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            with open(output_path, 'w') as f:
                for i in range(0, len(self.rom_data or b''), 4):
                    chunk = (self.rom_data or b'')[i:i + 4]
                    while len(chunk) < 4:
                        chunk += b'\x00'
                    le_word = f'{chunk[3]:02x}{chunk[2]:02x}{chunk[1]:02x}{chunk[0]:02x}'
                    f.write(f'{le_word}\n')
            logger.info(f'Saved ROM hex data to {output_path}')
            return True
        except Exception as e:
            logger.error(f'Failed to save ROM hex data: {e}')
            return False

    def get_rom_info(self) -> Dict[str, str]:
        """
        Get information about the ROM

        Returns:
            Dictionary with ROM information
        """
        if self.rom_data is None and self.rom_file_path:
            self.load_rom_file()
        info = {'rom_size': str(self.rom_size), 'rom_file': self.rom_file_path}
        if self.rom_data is not None:
            if len(self.rom_data) >= 2 and self.rom_data[0] == 85 and (self.rom_data[1] == 170):
                info['valid_signature'] = 'True'
            else:
                info['valid_signature'] = 'False'
            if len(self.rom_data) >= 3:
                rom_size_blocks = self.rom_data[2]
                rom_size_bytes = rom_size_blocks * 512
                info['rom_size_from_header'] = str(rom_size_bytes)
        return info

    def setup_option_rom(self, bdf: str, use_existing_rom: bool=False) -> Dict[str, str]:
        """
        Complete setup process: extract ROM, save hex file, and return info

        Args:
            bdf: PCIe Bus:Device.Function
            use_existing_rom: Use existing ROM file if available

        Returns:
            Dictionary with ROM information
        """
        try:
            if use_existing_rom and self.rom_file_path and os.path.exists(self.rom_file_path):
                logger.info(f'Using existing ROM file: {self.rom_file_path}')
                self.load_rom_file()
            else:
                success, rom_path = self.extract_rom_linux(bdf)
                if not success:
                    raise OptionROMError(f'Failed to extract ROM from {bdf}')
            hex_path = str(self.output_dir / 'rom_init.hex')
            if not self.save_rom_hex(hex_path):
                raise OptionROMError('Failed to save ROM hex file')
            return self.get_rom_info()
        except Exception as e:
            logger.error(f'Failed to setup Option-ROM: {e}')
            raise OptionROMError(f'Option-ROM setup failed: {e}')