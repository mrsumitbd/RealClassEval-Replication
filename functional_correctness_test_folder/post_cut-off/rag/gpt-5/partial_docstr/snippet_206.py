from pathlib import Path
from typing import List, Optional, Union


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
        # Mapping of standard PCI Type 0 configuration header dword offsets to descriptions.
        self._register_map = {
            0x00: 'Device/Vendor ID',
            0x04: 'Status/Command',
            0x08: 'Class Code/Subclass/ProgIF/Revision',
            0x0C: 'BIST/Header Type/Latency Timer/Cache Line Size',
            0x10: 'Base Address Register 0 (BAR0)',
            0x14: 'Base Address Register 1 (BAR1)',
            0x18: 'Base Address Register 2 (BAR2)',
            0x1C: 'Base Address Register 3 (BAR3)',
            0x20: 'Base Address Register 4 (BAR4)',
            0x24: 'Base Address Register 5 (BAR5)',
            0x28: 'CardBus CIS Pointer',
            0x2C: 'Subsystem ID/Subsystem Vendor ID',
            0x30: 'Expansion ROM Base Address',
            0x34: 'Capabilities Pointer',
            0x38: 'Reserved',
            0x3C: 'Max_Lat/Min_Gnt/Interrupt Pin/Interrupt Line',
        }

    def format_config_space_to_hex(
        self,
        config_space_data: bytes,
        include_comments: bool = True,
        words_per_line: int = 1,
        vendor_id: Optional[str] = None,
        device_id: Optional[str] = None,
        class_code: Optional[str] = None,
        board: Optional[str] = None
    ) -> str:
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
        if not isinstance(config_space_data, (bytes, bytearray)):
            raise ValueError('config_space_data must be bytes-like.')
        if words_per_line < 1:
            raise ValueError('words_per_line must be >= 1.')

        dwords = self.convert_to_dword_list(bytes(config_space_data))

        lines: List[str] = []
        if include_comments:
            meta_parts = []
            if vendor_id:
                meta_parts.append(f'Vendor={vendor_id}')
            if device_id:
                meta_parts.append(f'Device={device_id}')
            if class_code:
                meta_parts.append(f'Class={class_code}')
            if board:
                meta_parts.append(f'Board={board}')
            header = '// PCI Configuration Space ($readmemh)'
            if meta_parts:
                header += ' [' + ', '.join(meta_parts) + ']'
            lines.append(header)

        current_line_words: List[str] = []
        current_line_comments: List[str] = []
        for i, dword in enumerate(dwords):
            offset = i * 4
            current_line_words.append(f'{dword:08x}')
            if include_comments:
                reg_comment = self._get_register_comment(offset)
                if reg_comment:
                    current_line_comments.append(
                        f'0x{offset:03x}: {reg_comment}')
                else:
                    current_line_comments.append(f'0x{offset:03x}')

            line_full = (len(current_line_words) >=
                         words_per_line) or (i == len(dwords) - 1)
            if line_full:
                line = ' '.join(current_line_words)
                if include_comments and current_line_comments:
                    line += '  // ' + ' | '.join(current_line_comments)
                lines.append(line)
                current_line_words = []
                current_line_comments = []

        return '\n'.join(lines) + '\n'

    def _get_register_comment(self, offset: int) -> Optional[str]:
        '''
        Get a descriptive comment for a register offset.
        Args:
            offset: Register offset in configuration space
        Returns:
            Register description or None if no standard register
        '''
        return self._register_map.get(offset)

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
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        hex_str = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments)
        try:
            output.write_text(hex_str, encoding='utf-8')
        except OSError as e:
            raise IOError(f'Failed to write hex file: {e}') from e
        return output

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        '''
        Validate a hex file for proper formatting.
        Args:
            hex_file_path: Path to hex file to validate
        Returns:
            True if valid, False otherwise
        '''
        path = Path(hex_file_path)
        try:
            lines = path.read_text(encoding='utf-8').splitlines()
        except OSError:
            return False

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith('//'):
                continue
            # Remove trailing inline comment if present.
            if '//' in stripped:
                stripped = stripped.split('//', 1)[0].rstrip()
                if not stripped:
                    continue
            tokens = stripped.split()
            if not tokens:
                continue
            for tok in tokens:
                if not (1 <= len(tok) <= 8):
                    return False
                # Ensure hex digits only.
                for ch in tok:
                    if ch not in '0123456789abcdefABCDEF':
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
        if not isinstance(config_space_data, (bytes, bytearray)):
            raise ValueError('config_space_data must be bytes-like.')

        data = bytes(config_space_data)
        remainder = len(data) % 4
        if remainder:
            data += b'\x00' * (4 - remainder)

        dwords: List[int] = []
        for i in range(0, len(data), 4):
            dwords.append(int.from_bytes(
                data[i:i + 4], byteorder='little', signed=False))
        return dwords
