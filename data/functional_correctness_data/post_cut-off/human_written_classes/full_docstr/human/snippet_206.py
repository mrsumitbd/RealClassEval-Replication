import logging
from pathlib import Path
from typing import List, Optional, Union

class ConfigSpaceHexFormatter:
    """
    Formats PCI configuration space data into hex files for FPGA initialization.

    This class handles:
    - Converting configuration space bytes to little-endian 32-bit words
    - Generating properly formatted hex files for Vivado $readmemh
    - Adding debug comments with register offsets
    - Ensuring proper alignment and padding
    """
    REGISTER_NAMES = {0: 'Device/Vendor ID', 4: 'Status/Command', 8: 'Class Code/Revision ID', 12: 'BIST/Header Type/Latency Timer/Cache Line Size', 16: 'BAR0', 20: 'BAR1', 24: 'BAR2', 28: 'BAR3', 32: 'BAR4', 36: 'BAR5', 40: 'Cardbus CIS Pointer', 44: 'Subsystem ID/Subsystem Vendor ID', 48: 'Expansion ROM Base Address', 52: 'Capabilities Pointer', 56: 'Reserved', 60: 'Max_Lat/Min_Gnt/Interrupt Pin/Interrupt Line'}

    def __init__(self):
        """Initialize the hex formatter."""
        self.logger = logging.getLogger(__name__)

    def format_config_space_to_hex(self, config_space_data: bytes, include_comments: bool=True, words_per_line: int=1, vendor_id: Optional[str]=None, device_id: Optional[str]=None, class_code: Optional[str]=None, board: Optional[str]=None) -> str:
        """
        Convert configuration space data to hex format.

        Args:
            config_space_data: Raw configuration space bytes
            include_comments: Whether to include offset/register comments
            words_per_line: Number of 32-bit words per line (default: 1)

        Returns:
            Formatted hex string suitable for $readmemh

        Raises:
            ValueError: If config space data is invalid
        """
        if not config_space_data:
            raise ValueError('Configuration space data cannot be empty')
        if len(config_space_data) % 4 != 0:
            padding_bytes = 4 - len(config_space_data) % 4
            log_info_safe(self.logger, 'Padding config space with {padding} zero bytes for alignment', padding=padding_bytes, prefix='HEX')
            config_space_data = config_space_data + bytes(padding_bytes)
        hex_lines = []
        if include_comments:
            from src.string_utils import generate_hex_header_comment
            header = generate_hex_header_comment(title='config_space_init.hex - PCIe Configuration Space Initialization', total_bytes=len(config_space_data), total_dwords=len(config_space_data) // 4, vendor_id=vendor_id, device_id=device_id, class_code=class_code, board=board)
            hex_lines.append(header)
            hex_lines.append('')
        for offset in range(0, len(config_space_data), 4):
            if offset + 4 <= len(config_space_data):
                word_bytes = config_space_data[offset:offset + 4]
            else:
                word_bytes = config_space_data[offset:]
                word_bytes += bytes(4 - len(word_bytes))
            word_value = int.from_bytes(word_bytes, byteorder='little')
            hex_word = f'{word_value:08X}'
            if include_comments:
                comment = self._get_register_comment(offset)
                if comment:
                    hex_lines.append(f'// Offset 0x{offset:03X} - {comment}')
            hex_lines.append(hex_word)
            if include_comments and offset in [60, 252, 1020]:
                hex_lines.append('')
        return '\n'.join(hex_lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        """
        Get a descriptive comment for a register offset.

        Args:
            offset: Register offset in configuration space

        Returns:
            Register description or None if no standard register
        """
        if offset in self.REGISTER_NAMES:
            return self.REGISTER_NAMES[offset]
        if 64 <= offset < 256:
            return f'Capability at 0x{offset:02X}'
        elif 256 <= offset < 4096:
            return f'Extended Capability at 0x{offset:03X}'
        return None

    def write_hex_file(self, config_space_data: bytes, output_path: Union[str, Path], include_comments: bool=True) -> Path:
        """
        Write configuration space data to a hex file.

        Args:
            config_space_data: Raw configuration space bytes
            output_path: Path where hex file should be written
            include_comments: Whether to include offset/register comments

        Returns:
            Path to the written hex file

        Raises:
            IOError: If file cannot be written
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        hex_content = self.format_config_space_to_hex(config_space_data, include_comments=include_comments)
        try:
            with open(output_path, 'w') as f:
                f.write(hex_content)
            log_info_safe(self.logger, 'Written configuration space hex file: {path}', path=output_path, prefix='HEX')
            return output_path
        except IOError as e:
            log_error_safe(self.logger, 'Failed to write hex file {path}: {error}', path=output_path, error=str(e), prefix='HEX')
            raise

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        """
        Validate a hex file for proper formatting.

        Args:
            hex_file_path: Path to hex file to validate

        Returns:
            True if valid, False otherwise
        """
        hex_file_path = Path(hex_file_path)
        if not hex_file_path.exists():
            log_error_safe(self.logger, 'Hex file does not exist: {path}', path=hex_file_path, prefix='HEX')
            return False
        try:
            with open(hex_file_path, 'r') as f:
                lines = f.readlines()
            hex_word_count = 0
            for line in lines:
                line = line.strip()
                if not line or line.startswith('//'):
                    continue
                if len(line) != 8:
                    log_error_safe(self.logger, 'Invalid hex word length in line: {line}', line=line, prefix='HEX')
                    return False
                try:
                    int(line, 16)
                    hex_word_count += 1
                except ValueError:
                    log_error_safe(self.logger, 'Invalid hex characters in line: {line}', line=line, prefix='HEX')
                    return False
            log_info_safe(self.logger, 'Hex file validated successfully: {words} words', words=hex_word_count, prefix='HEX')
            return True
        except IOError as e:
            log_error_safe(self.logger, 'Failed to read hex file {path}: {error}', path=hex_file_path, error=str(e), prefix='HEX')
            return False

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        """
        Convert configuration space bytes to a list of 32-bit dwords.

        Args:
            config_space_data: Raw configuration space bytes

        Returns:
            List of 32-bit integers in little-endian format
        """
        dwords = []
        if len(config_space_data) % 4 != 0:
            padding_bytes = 4 - len(config_space_data) % 4
            config_space_data = config_space_data + bytes(padding_bytes)
        for offset in range(0, len(config_space_data), 4):
            word_bytes = config_space_data[offset:offset + 4]
            dword = int.from_bytes(word_bytes, byteorder='little')
            dwords.append(dword)
        return dwords