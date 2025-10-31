
from typing import Optional, Union, List
from pathlib import Path


class ConfigSpaceHexFormatter:
    '''
    Formats PCI configuration space data into hex files for FPGA initialization.
    This class handles:
    - Converting configuration space bytes to little-endian 32-bit words
    - Generating properly formatted hex files for Vivado $readmemh
    - Adding debug comments with register offsets
    - Ensuring proper alignment and padding
    '''

    def __init__(self):
        '''Initialize the hex formatter.'''
        self._register_descriptions = {
            0x00: 'Vendor ID',
            0x02: 'Device ID',
            0x04: 'Command',
            0x06: 'Status',
            0x08: 'Revision ID',
            0x09: 'Class Code',
            0x0C: 'Cache Line Size',
            0x0D: 'Latency Timer',
            0x0E: 'Header Type',
            0x0F: 'BIST',
            0x10: 'Base Address 0',
            0x14: 'Base Address 1',
            0x18: 'Base Address 2',
            0x1C: 'Base Address 3',
            0x20: 'Base Address 4',
            0x24: 'Base Address 5',
            0x2C: 'Subsystem Vendor ID',
            0x2E: 'Subsystem ID',
            0x34: 'Capabilities Pointer',
            0x3C: 'Interrupt Line',
            0x3D: 'Interrupt Pin'
        }

    def format_config_space_to_hex(self, config_space_data: bytes, include_comments: bool = True, words_per_line: int = 1, vendor_id: Optional[str] = None, device_id: Optional[str] = None, class_code: Optional[str] = None, board: Optional[str] = None) -> str:
        '''
        Convert configuration space data to hex format.
        Args:
            config_space_data: Raw configuration space bytes
            include_comments: Whether to include offset/register comments
            words_per_line: Number of 32-bit words per line (default: 1)
        Returns:
            Formatted hex string suitable for $readmemh
        Raises:
            ValueError: If config space data is invalid
        '''
        if len(config_space_data) % 4 != 0:
            raise ValueError('Config space data must be a multiple of 4 bytes')

        dword_list = self.convert_to_dword_list(config_space_data)
        hex_lines = []
        for i, dword in enumerate(dword_list):
            hex_line = f'{dword:08x}'
            if include_comments:
                comment = self._get_register_comment(i * 4)
                if comment:
                    hex_line += f' // {comment} (Offset: {i*4:02x})'
                else:
                    hex_line += f' // Offset: {i*4:02x}'
            hex_lines.append(hex_line)

        formatted_hex = '\n'.join([f'{line}' for line in hex_lines])
        return formatted_hex

    def _get_register_comment(self, offset: int) -> Optional[str]:
        '''
        Get a descriptive comment for a register offset.
        Args:
            offset: Register offset in configuration space
        Returns:
            Register description or None if no standard register
        '''
        return self._register_descriptions.get(offset)

    def write_hex_file(self, config_space_data: bytes, output_path: Union[str, Path], include_comments: bool = True) -> Path:
        '''
        Write configuration space data to a hex file.
        Args:
            config_space_data: Raw configuration space bytes
            output_path: Path where hex file should be written
            include_comments: Whether to include offset/register comments
        Returns:
            Path to the written hex file
        Raises:
            IOError: If file cannot be written
        '''
        output_path = Path(output_path)
        try:
            with open(output_path, 'w') as f:
                f.write(self.format_config_space_to_hex(
                    config_space_data, include_comments))
        except IOError as e:
            raise IOError(f'Failed to write hex file: {e}')
        return output_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        '''
        Validate a hex file for proper formatting.
        Args:
            hex_file_path: Path to hex file to validate
        Returns:
            True if valid, False otherwise
        '''
        hex_file_path = Path(hex_file_path)
        try:
            with open(hex_file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip().split('//')[0].strip()
                    if not line or len(line) != 8:
                        return False
                    try:
                        int(line, 16)
                    except ValueError:
                        return False
        except IOError:
            return False
        return True

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        '''
        Convert configuration space bytes to a list of 32-bit dwords.
        Args:
            config_space_data: Raw configuration space bytes
        Returns:
            List of 32-bit integers in little-endian format
        '''
        dword_list = []
        for i in range(0, len(config_space_data), 4):
            dword = int.from_bytes(config_space_data[i:i+4], 'little')
            dword_list.append(dword)
        return dword_list
