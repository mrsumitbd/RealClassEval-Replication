
class OptionROMManager:
    '''Manager for Option-ROM extraction and handling'''

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        '''
        Initialize the Option-ROM manager
        Args:
            output_dir: Path to directory for storing extracted ROM
            rom_file_path: Path to an existing ROM file to use instead of extraction
        '''
        self.output_dir = output_dir or Path.cwd()
        self.rom_file_path = rom_file_path
        self.rom_data = None
        self.rom_info = {}

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        '''
        Extract Option-ROM from a PCI device on Linux
        Args:
            bdf: PCIe Bus:Device.Function (e.g., "0000:03:00.0")
        Returns:
            Tuple of (success, rom_path)
        '''
        rom_path = self.output_dir / f"{bdf.replace(':', '_')}_rom.bin"
        try:
            with open(rom_path, 'wb') as f:
                subprocess.run(
                    ['setpci', '-s', bdf, 'ECAP_VSEC+0x10.L'], stdout=f, check=True)
            self.rom_file_path = str(rom_path)
            return (True, str(rom_path))
        except subprocess.CalledProcessError as e:
            print(f"Failed to extract ROM: {e}")
            return (False, "")

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        '''
        Load ROM data from a file
        Args:
            file_path: Path to ROM file (uses self.rom_file_path if None)
        Returns:
            True if ROM was loaded successfully
        '''
        file_path = file_path or self.rom_file_path
        if not file_path:
            return False

        try:
            with open(file_path, 'rb') as f:
                self.rom_data = f.read()
            self.rom_info['size'] = len(self.rom_data)
            self.rom_info['file_path'] = file_path
            return True
        except IOError as e:
            print(f"Failed to load ROM file: {e}")
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

        output_path = output_path or str(self.output_dir / "rom_init.hex")
        try:
            with open(output_path, 'w') as f:
                for i in range(0, len(self.rom_data), 16):
                    chunk = self.rom_data[i:i+16]
                    hex_line = ' '.join(f"{byte:02x}" for byte in chunk)
                    f.write(f"{hex_line}\n")
            self.rom_info['hex_path'] = output_path
            return True
        except IOError as e:
            print(f"Failed to save hex file: {e}")
            return False

    def get_rom_info(self) -> Dict[str, str]:
        '''
        Get information about the ROM
        Returns:
            Dictionary with ROM information
        '''
        return self.rom_info

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
            success = self.load_rom_file()
        else:
            success, rom_path = self.extract_rom_linux(bdf)
            if success:
                success = self.load_rom_file(rom_path)

        if success:
            self.save_rom_hex()

        return self.get_rom_info()
