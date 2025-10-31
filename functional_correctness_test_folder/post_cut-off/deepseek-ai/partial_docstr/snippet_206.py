
from typing import Optional, Union, List
from pathlib import Path


class ConfigSpaceHexFormatter:

    def __init__(self):
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

        for i in range(0, len(dwords), words_per_line):
            line_dwords = dwords[i:i + words_per_line]
            hex_parts = [f"{dword:08x}" for dword in line_dwords]
            line = " ".join(hex_parts)

            if include_comments:
                comments = []
                for j in range(words_per_line):
                    offset = (i + j) * 4
                    if offset < len(config_space_data):
                        comment = self._get_register_comment(offset)
                        if comment:
                            comments.append(f"// {offset:03x}: {comment}")
                if comments:
                    line += " " + " ".join(comments)

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
        register_comments = {
            0x00: "Vendor ID",
            0x04: "Device ID",
            0x08: "Command/Status",
            0x0C: "Class Code/Revision",
            0x10: "BIST/Header Type/Latency Timer/Cache Line Size",
            0x14: "BAR0",
            0x18: "BAR1",
            0x1C: "BAR2",
            0x20: "BAR3",
            0x24: "BAR4",
            0x28: "BAR5",
            0x2C: "Cardbus CIS Pointer",
            0x30: "Subsystem Vendor ID",
            0x34: "Subsystem ID",
            0x38: "Expansion ROM Base Address",
            0x3C: "Capabilities Pointer/Interrupt Line/Pin/Min_Gnt/Max_Lat",
        }
        return register_comments.get(offset)

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
            with open(output_path, 'w') as f:
                f.write(hex_content)
        except IOError as e:
            raise IOError(f"Failed to write hex file: {e}")

        return output_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        try:
            with open(hex_file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('//'):
                        parts = line.split()
                        for part in parts:
                            if part.startswith('//'):
                                break
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
        if len(config_space_data) % 4 != 0:
            raise ValueError(
                "Configuration space data must be a multiple of 4 bytes")

        dwords = []
        for i in range(0, len(config_space_data), 4):
            word = config_space_data[i:i+4]
            dword = int.from_bytes(word, byteorder='little')
            dwords.append(dword)
        return dwords
