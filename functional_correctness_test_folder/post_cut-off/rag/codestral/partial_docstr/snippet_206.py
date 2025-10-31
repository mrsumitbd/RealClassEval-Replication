
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
        0x10: "BIST",
        0x14: "Base Address Register 0",
        0x18: "Base Address Register 1",
        0x1C: "Base Address Register 2",
        0x20: "Base Address Register 3",
        0x24: "Base Address Register 4",
        0x28: "Base Address Register 5",
        0x2C: "Cardbus CIS Pointer",
        0x30: "Subsystem Vendor ID",
        0x32: "Subsystem ID",
        0x34: "Expansion ROM Base Address",
        0x3C: "Interrupt Line",
        0x3D: "Interrupt Pin",
        0x3E: "Minimum Grant",
        0x3F: "Maximum Latency"
    }

    def __init__(self):
        '''Initialize the hex formatter.'''
        pass

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

        dwords = self.convert_to_dword_list(config_space_data)
        hex_lines = []

        if vendor_id or device_id or class_code or board:
            hex_lines.append(f"// PCI Device Information")
            if vendor_id:
                hex_lines.append(f"// Vendor ID: {vendor_id}")
            if device_id:
                hex_lines.append(f"// Device ID: {device_id}")
            if class_code:
                hex_lines.append(f"// Class Code: {class_code}")
            if board:
                hex_lines.append(f"// Board: {board}")
            hex_lines.append("")

        for i, dword in enumerate(dwords):
            offset = i * 4
            hex_value = f"{dword:08X}"

            line = hex_value
            if include_comments:
                comment = self._get_register_comment(offset)
                if comment:
                    line += f" // {comment}"

            hex_lines.append(line)

        # Group words per line if requested
        if words_per_line > 1:
            grouped_lines = []
            for i in range(0, len(hex_lines), words_per_line):
                group = hex_lines[i:i+words_per_line]
                grouped_lines.append(" ".join(group))
            hex_lines = grouped_lines

        return "\n".join(hex_lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        '''
        Get a descriptive comment for a register offset.
        Args:
            offset: Register offset in configuration space
        Returns:
            Register description or None if no standard register
        '''
        return self._STANDARD_REGISTERS.get(offset, None)

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

                # Check for valid hex values
                parts = line.split()
                for part in parts:
                    if part.startswith("//"):
                        continue
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
                chunk += b'\x00' * (4 - len(chunk))  # Pad with zeros if needed
            dword = struct.unpack('<I', chunk)[0]
            dwords.append(dword)
        return dwords
