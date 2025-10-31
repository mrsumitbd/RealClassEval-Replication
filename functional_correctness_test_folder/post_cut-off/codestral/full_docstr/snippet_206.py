
import struct
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
        self.register_comments = {
            0x00: "Vendor ID",
            0x02: "Device ID",
            0x04: "Command Register",
            0x06: "Status Register",
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

        dword_list = self.convert_to_dword_list(config_space_data)
        hex_lines = []

        if vendor_id or device_id or class_code or board:
            hex_lines.append(
                f"// Vendor ID: {vendor_id if vendor_id else 'N/A'}")
            hex_lines.append(
                f"// Device ID: {device_id if device_id else 'N/A'}")
            hex_lines.append(
                f"// Class Code: {class_code if class_code else 'N/A'}")
            hex_lines.append(f"// Board: {board if board else 'N/A'}")
            hex_lines.append("")

        for i, dword in enumerate(dword_list):
            offset = i * 4
            hex_line = f"@{offset:04X} {dword:08X}"

            if include_comments:
                comment = self._get_register_comment(offset)
                if comment:
                    hex_line += f" // {comment}"

            hex_lines.append(hex_line)

        return "\n".join(hex_lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        '''
        Get a descriptive comment for a register offset.
        Args:
            offset: Register offset in configuration space
        Returns:
            Register description or None if no standard register
        '''
        return self.register_comments.get(offset, None)

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
        hex_file_path = Path(hex_file_path)

        try:
            with open(hex_file_path, 'r') as f:
                lines = f.readlines()
        except IOError:
            return False

        for line in lines:
            line = line.strip()
            if not line or line.startswith("//"):
                continue

            parts = line.split()
            if len(parts) < 2:
                return False

            if not parts[0].startswith("@") or not parts[0][1:].isdigit():
                return False

            if not all(part.isdigit() for part in parts[1:]):
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
            dword_bytes = config_space_data[i:i+4]
            dword = struct.unpack('<I', dword_bytes)[0]
            dword_list.append(dword)
        return dword_list
