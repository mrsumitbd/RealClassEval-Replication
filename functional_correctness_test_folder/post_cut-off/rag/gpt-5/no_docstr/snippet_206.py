from pathlib import Path
from typing import List, Optional, Union
import datetime
import os
import re


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
        self._register_names = {
            0x00: 'Vendor ID / Device ID',
            0x04: 'Command / Status',
            0x08: 'Revision ID / Prog IF / Subclass / Class Code',
            0x0C: 'Cache Line / Latency / Header Type / BIST',
            0x10: 'BAR0',
            0x14: 'BAR1',
            0x18: 'BAR2',
            0x1C: 'BAR3',
            0x20: 'BAR4',
            0x24: 'BAR5',
            0x28: 'CardBus CIS Pointer',
            0x2C: 'Subsystem Vendor ID / Subsystem ID',
            0x30: 'Expansion ROM Base Address',
            0x34: 'Capabilities Pointer',
            0x38: 'Reserved',
            0x3C: 'Interrupt Line / Interrupt Pin / Min_Gnt / Max_Lat',
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
            raise ValueError('config_space_data must be bytes')
        if len(config_space_data) == 0:
            raise ValueError('config_space_data cannot be empty')
        if words_per_line < 1:
            raise ValueError('words_per_line must be >= 1')

        dwords = self.convert_to_dword_list(config_space_data)

        header_lines = []
        if include_comments:
            ts = datetime.datetime.now().isoformat(timespec='seconds')
            header_lines.append(
                f'// PCI Configuration Space Hex - generated {ts}')
            # Try to extract IDs if not provided
            try:
                first = dwords[0]
                extracted_vendor = f'0x{first & 0xFFFF:04x}'
                extracted_device = f'0x{(first >> 16) & 0xFFFF:04x}'
            except Exception:
                extracted_vendor = None
                extracted_device = None

            if vendor_id is None and extracted_vendor is not None:
                vendor_id = extracted_vendor
            if device_id is None and extracted_device is not None:
                device_id = extracted_device

            # Class code (upper 3 bytes of dword at 0x08)
            if class_code is None and len(dwords) > 2:
                cc_dword = dwords[2]
                cc_val = (cc_dword >> 8) & 0xFFFFFF
                class_code = f'0x{cc_val:06x}'

            if vendor_id:
                header_lines.append(f'// Vendor ID: {vendor_id}')
            if device_id:
                header_lines.append(f'// Device ID: {device_id}')
            if class_code:
                header_lines.append(f'// Class Code: {class_code}')
            if board:
                header_lines.append(f'// Board: {board}')

        lines = []
        if header_lines:
            lines.extend(header_lines)

        # Build data lines
        for i in range(0, len(dwords), words_per_line):
            chunk = dwords[i:i + words_per_line]
            tokens = [f'{val:08x}' for val in chunk]
            line = ' '.join(tokens)

            if include_comments:
                # Compose a compact comment describing the offsets and registers in this line
                comments = []
                for j in range(len(chunk)):
                    offset = (i + j) * 4
                    reg = self._get_register_comment(offset)
                    if reg:
                        comments.append(f'0x{offset:04x}: {reg}')
                    else:
                        comments.append(f'0x{offset:04x}')
                if comments:
                    line = f'{line} // ' + ' | '.join(comments)

            lines.append(line)

        return '\n'.join(lines) + '\n'

    def _get_register_comment(self, offset: int) -> Optional[str]:
        '''
        Get a descriptive comment for a register offset.
        Args:
            offset: Register offset in configuration space
        Returns:
            Register description or None if no standard register
        '''
        return self._register_names.get(offset)

    def write_hex_file(
        self,
        config_space_data: bytes,
        output_path: Union[str, Path],
        include_comments: bool = True
    ) -> Path:
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
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        text = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments)
        try:
            out_path.write_text(text, encoding='utf-8', newline='\n')
        except OSError as e:
            raise IOError(f'Failed to write hex file: {e}') from e
        return out_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        '''
        Validate a hex file for proper formatting.
        Args:
            hex_file_path: Path to hex file to validate
        Returns:
            True if valid, False otherwise
        '''
        path = Path(hex_file_path)
        if not path.is_file():
            return False

        hex_re = re.compile(r'^[0-9a-fA-F]{1,8}$')
        try:
            with path.open('r', encoding='utf-8') as f:
                for line in f:
                    line = line.rstrip('\n')
                    # Remove comments
                    if '//' in line:
                        line = line[:line.index('//')]
                    line = line.strip()
                    if not line:
                        continue
                    tokens = line.split()
                    for tok in tokens:
                        if not hex_re.match(tok):
                            return False
            return True
        except OSError:
            return False

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        '''
        Convert configuration space bytes to a list of 32-bit dwords.
        Args:
            config_space_data: Raw configuration space bytes
        Returns:
            List of 32-bit integers in little-endian format
        '''
        if not isinstance(config_space_data, (bytes, bytearray)):
            raise ValueError('config_space_data must be bytes')

        data = bytes(config_space_data)
        rem = len(data) % 4
        if rem != 0:
            data += b'\x00' * (4 - rem)

        dwords: List[int] = []
        for i in range(0, len(data), 4):
            dwords.append(int.from_bytes(
                data[i:i + 4], byteorder='little', signed=False))
        return dwords
