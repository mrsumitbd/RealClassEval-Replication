
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
            raise ValueError("Configuration space data must be 32-bit aligned")

        dwords = self.convert_to_dword_list(config_space_data)
        hex_lines = []

        if include_comments:
            header_comment = "// PCIe Configuration Space"
            if vendor_id:
                header_comment += f" VID: {vendor_id}"
            if device_id:
                header_comment += f" DID: {device_id}"
            if class_code:
                header_comment += f" Class: {class_code}"
            if board:
                header_comment += f" Board: {board}"
            hex_lines.append(header_comment)

        for i in range(0, len(dwords), words_per_line):
            line_dwords = dwords[i:i+words_per_line]
            hex_words = [f"{dword:08x}" for dword in line_dwords]
            line = " ".join(hex_words)

            if include_comments:
                offset = i * 4
                comment = f" // Offset 0x{offset:03x}"
                register_comment = self._get_register_comment(offset)
                if register_comment:
                    comment += f": {register_comment}"
                line += comment

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
        # Standard PCIe register offsets
        register_map = {
            0x00: "Vendor ID",
            0x02: "Device ID",
            0x04: "Command",
            0x06: "Status",
            0x08: "Revision ID / Class Code",
            0x0C: "Cache Line Size / Latency Timer / Header Type / BIST",
            0x10: "BAR0",
            0x14: "BAR1",
            0x18: "BAR2",
            0x1C: "BAR3",
            0x20: "BAR4",
            0x24: "BAR5",
            0x28: "Cardbus CIS Pointer",
            0x2C: "Subsystem Vendor ID",
            0x2E: "Subsystem ID",
            0x30: "Expansion ROM Base Address",
            0x34: "Capabilities Pointer",
            0x3C: "Interrupt Line / Pin / Min_Gnt / Max_Lat",
        }
        return register_map.get(offset)

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
        hex_content = self.format_config_space_to_hex(
            config_space_data, include_comments)
        output_path = Path(output_path)

        try:
            with output_path.open('w') as f:
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
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('//'):
                        continue
                    for word in line.split():
                        if not all(c in '0123456789abcdefABCDEF' for c in word):
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
            word_bytes = config_space_data[i:i+4]
            if len(word_bytes) < 4:
                word_bytes += b'\x00' * (4 - len(word_bytes))
            dword = struct.unpack('<I', word_bytes)[0]
            dwords.append(dword)
        return dwords
