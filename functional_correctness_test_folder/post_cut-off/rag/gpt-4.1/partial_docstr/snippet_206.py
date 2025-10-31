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

    # PCI config space register map for comments (offset: description)
    _REGISTER_MAP = {
        0x00: "Device/Vendor ID",
        0x04: "Status/Command",
        0x08: "Class Code/Revision ID",
        0x0C: "BIST/Header Type/Latency Timer/Cache Line Size",
        0x10: "BAR0",
        0x14: "BAR1",
        0x18: "BAR2",
        0x1C: "BAR3",
        0x20: "BAR4",
        0x24: "BAR5",
        0x28: "Cardbus CIS Pointer",
        0x2C: "Subsystem ID/Vendor ID",
        0x30: "Expansion ROM Base Address",
        0x34: "Capabilities Pointer",
        0x38: "Reserved",
        0x3C: "Interrupt Line/Pin/Min_Gnt/Max_Lat",
        # Add more as needed
    }

    def __init__(self):
        '''Initialize the hex formatter.'''
        pass

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
            raise ValueError("config_space_data must be bytes or bytearray")
        if len(config_space_data) == 0:
            raise ValueError("config_space_data is empty")
        if words_per_line < 1:
            raise ValueError("words_per_line must be >= 1")

        dwords = self.convert_to_dword_list(config_space_data)
        lines = []

        # Optional header comment
        if include_comments:
            header = "// PCI Config Space Hex File"
            if board:
                header += f" for {board}"
            lines.append(header)
            if vendor_id or device_id or class_code:
                id_line = "//"
                if vendor_id:
                    id_line += f" VendorID: {vendor_id}"
                if device_id:
                    id_line += f" DeviceID: {device_id}"
                if class_code:
                    id_line += f" ClassCode: {class_code}"
                lines.append(id_line)
            lines.append("// Format: <hex dword(s)> // <offset> <register>")

        for i in range(0, len(dwords), words_per_line):
            word_group = dwords[i:i+words_per_line]
            offset = i * 4
            hex_words = " ".join(f"{w:08x}" for w in word_group)
            comment = ""
            if include_comments:
                comment_parts = []
                for j, _ in enumerate(word_group):
                    reg_offset = offset + j*4
                    reg_comment = self._get_register_comment(reg_offset)
                    if reg_comment:
                        comment_parts.append(
                            f"0x{reg_offset:02X}: {reg_comment}")
                if comment_parts:
                    comment = " // " + ", ".join(comment_parts)
                else:
                    comment = f" // 0x{offset:02X}"
            line = hex_words + (comment if include_comments else "")
            lines.append(line)

        return "\n".join(lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        '''
        Get a descriptive comment for a register offset.
        Args:
            offset: Register offset in configuration space
        Returns:
            Register description or None if no standard register
        '''
        return self._REGISTER_MAP.get(offset)

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
        hex_str = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments)
        path = Path(output_path)
        try:
            with path.open("w", encoding="utf-8") as f:
                f.write(hex_str)
        except Exception as e:
            raise IOError(f"Failed to write hex file: {e}")
        return path

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
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("//"):
                        continue
                    # Remove comments
                    if "//" in line:
                        line = line.split("//", 1)[0].strip()
                    if not line:
                        continue
                    words = line.split()
                    for word in words:
                        if len(word) != 8:
                            return False
                        int(word, 16)  # will raise if not hex
            return True
        except Exception:
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
        data = config_space_data
        # Pad to multiple of 4 bytes
        if len(data) % 4 != 0:
            data += b'\x00' * (4 - (len(data) % 4))
        for i in range(0, len(data), 4):
            dword = int.from_bytes(data[i:i+4], byteorder='little')
            dwords.append(dword)
        return dwords
