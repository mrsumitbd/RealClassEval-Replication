
from pathlib import Path
from typing import List, Optional, Union
import struct


class ConfigSpaceHexFormatter:
    '''
    Formats PCI configuration space data into hex files for FPGA initialization.
    This class handles:
    - Converting configuration space bytes to little-endian 32-bit words
    - Generating properly formatted hex files for Vivado $readmemh
    - Adding debug comments with register offsets
    - Ensuring proper alignment and padding
    '''

    _STANDARD_REGISTERS = {
        0x00: "Vendor ID",
        0x02: "Device ID",
        0x04: "Command",
        0x06: "Status",
        0x08: "Revision ID",
        0x09: "Class Code",
        0x0A: "Subclass",
        0x0B: "Prog IF",
        0x0C: "Cache Line Size",
        0x0D: "Latency Timer",
        0x0E: "Header Type",
        0x0F: "BIST",
        0x10: "Base Address Register 0",
        0x14: "Base Address Register 1",
        0x18: "Base Address Register 2",
        0x1C: "Base Address Register 3",
        0x20: "Base Address Register 4",
        0x24: "Base Address Register 5",
        0x28: "Cardbus CIS Pointer",
        0x2C: "Subsystem Vendor ID",
        0x2E: "Subsystem ID",
        0x30: "Expansion ROM Base Address",
        0x3C: "Interrupt Line",
        0x3D: "Interrupt Pin",
        0x3E: "Minimum Grant",
        0x3F: "Maximum Latency"
    }

    def __init__(self):
        '''Initialize the hex formatter.'''
        self.vendor_id = None
        self.device_id = None
        self.class_code = None
        self.board = None

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
            raise ValueError(
                "Configuration space data must be a multiple of 4 bytes")

        self.vendor_id = vendor_id
        self.device_id = device_id
        self.class_code = class_code
        self.board = board

        dwords = self.convert_to_dword_list(config_space_data)
        hex_lines = []

        if include_comments and (vendor_id or device_id or class_code or board):
            header_comments = []
            if vendor_id:
                header_comments.append(f"Vendor ID: {vendor_id}")
            if device_id:
                header_comments.append(f"Device ID: {device_id}")
            if class_code:
                header_comments.append(f"Class Code: {class_code}")
            if board:
                header_comments.append(f"Board: {board}")
            hex_lines.append(f"// {' | '.join(header_comments)}")

        for i in range(0, len(dwords), words_per_line):
            chunk = dwords[i:i+words_per_line]
            hex_values = [f"{dword:08X}" for dword in chunk]
            line = " ".join(hex_values)

            if include_comments:
                offset = i * 4
                comment = self._get_register_comment(offset)
                if comment:
                    line += f" // {offset:02X}h: {comment}"

            hex_lines.append(line)

        return "\n".join(hex_lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        '''
        Get a descriptive comment for a register offset.
        Args:
            offset: Register offset in configuration space
        Returns:
            Register description or None if no standard register
        '''
        if offset in self._STANDARD_REGISTERS:
            return self._STANDARD_REGISTERS[offset]
        return None

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
        hex_content = self.format_config_space_to_hex(
            config_space_data, include_comments)

        try:
            with open(output_path, 'w') as f:
                f.write(hex_content)
        except IOError as e:
            raise IOError(f"Failed to write hex file: {e}")

        return output_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        '''
        Validate a hex file for proper formatting.
        Args:
            hex_file_path: Path to hex file to validate
        Returns:
            True if valid, False otherwise
        '''
        try:
            with open(hex_file_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()
                if not line or line.startswith("//"):
                    continue

                parts = line.split("//")[0].strip().split()
                for part in parts:
                    if not part or len(part) != 8:
                        return False
                    try:
                        int(part, 16)
                    except ValueError:
                        return False

            return True
        except IOError:
            return False

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        '''
        Convert configuration space bytes to a list of 32-bit dwords.
        Args:
            config_space_data: Raw configuration space bytes
        Returns:
            List of 32-bit integers in little-endian format
        '''
        dwords = []
        for i in range(0, len(config_space_data), 4):
            chunk = config_space_data[i:i+4]
            if len(chunk) < 4:
                chunk += b'\x00' * (4 - len(chunk))
            dword = struct.unpack('<I', chunk)[0]
            dwords.append(dword)
        return dwords
