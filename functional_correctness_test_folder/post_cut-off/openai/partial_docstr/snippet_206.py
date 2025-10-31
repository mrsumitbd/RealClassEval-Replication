
from pathlib import Path
from typing import List, Optional, Union


class ConfigSpaceHexFormatter:
    """
    Utility class for converting PCI configuration space data to a hex
    representation suitable for $readmemh and for validating such files.
    """

    # Standard PCI configuration register descriptions
    _REGISTER_DESCRIPTIONS = {
        0x00: "Vendor ID",
        0x02: "Device ID",
        0x04: "Command",
        0x06: "Status",
        0x08: "Revision ID",
        0x09: "Prog IF",
        0x0A: "Subclass",
        0x0B: "Base Class",
        0x0C: "Cache Line Size",
        0x0D: "Latency Timer",
        0x0E: "Header Type",
        0x0F: "BIST",
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
        0x3C: "Interrupt Line",
        0x3D: "Interrupt Pin",
        0x3E: "Minimum Grant",
        0x3F: "Maximum Latency",
    }

    def __init__(self):
        pass

    def format_config_space_to_hex(
        self,
        config_space_data: bytes,
        include_comments: bool = True,
        words_per_line: int = 1,
        vendor_id: Optional[str] = None,
        device_id: Optional[str] = None,
        class_code: Optional[str] = None,
        board: Optional[str] = None,
    ) -> str:
        """
        Convert configuration space data to hex format.
        """
        if len(config_space_data) % 4 != 0:
            raise ValueError(
                "Configuration space data length must be a multiple of 4 bytes.")

        lines: List[str] = []

        # Header comments
        if vendor_id or device_id or class_code or board:
            header = "// "
            if vendor_id:
                header += f"Vendor ID: {vendor_id} "
            if device_id:
                header += f"Device ID: {device_id} "
            if class_code:
                header += f"Class Code: {class_code} "
            if board:
                header += f"Board: {board}"
            lines.append(header.strip())

        total_words = len(config_space_data) // 4
        for word_index in range(0, total_words, words_per_line):
            line_parts: List[str] = []
            for i in range(words_per_line):
                idx = word_index + i
                if idx >= total_words:
                    break
                offset = idx * 4
                word_bytes = config_space_data[offset: offset + 4]
                word = int.from_bytes(word_bytes, byteorder="little")
                hex_str = f"0x{word:08x}"
                if include_comments:
                    comment = self._get_register_comment(offset)
                    if comment:
                        hex_str += f" // {comment}"
                line_parts.append(hex_str)
            lines.append(" ".join(line_parts))

        return "\n".join(lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        """
        Get a descriptive comment for a register offset.
        """
        return self._REGISTER_DESCRIPTIONS.get(offset)

    def write_hex_file(
        self,
        config_space_data: bytes,
        output_path: Union[str, Path],
        include_comments: bool = True,
    ) -> Path:
        """
        Write configuration space data to a hex file.
        """
        path = Path(output_path)
        hex_str = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments
        )
        try:
            path.write_text(hex_str, encoding="utf-8")
        except Exception as e:
            raise IOError(f"Failed to write hex file: {e}") from e
        return path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        """
        Validate that a hex file contains only 32‑bit hex values.
        """
        path = Path(hex_file_path)
        if not path.is_file():
            return False
        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.split("//")[0].strip()
                    if not line:
                        continue
                    # Accept both 0x prefix and plain hex
                    if line.lower().startswith("0x"):
                        line = line[2:]
                    if len(line) != 8:
                        return False
                    int(line, 16)
            return True
        except Exception:
            return False

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        """
        Convert configuration space bytes to a list of 32-bit dwords.
        """
        if len(config_space_data) % 4 != 0:
            raise ValueError(
                "Configuration space data length must be a multiple of 4 bytes.")
        return [
            int.from_bytes(config_space_data[i: i + 4], byteorder="little")
            for i in range(0, len(config_space_data), 4)
        ]
