
from typing import Optional, Union, List
from pathlib import Path


class ConfigSpaceHexFormatter:

    # Standard PCI config space register descriptions (offset: description)
    _REGISTER_COMMENTS = {
        0x00: "Vendor ID / Device ID",
        0x04: "Command / Status",
        0x08: "Revision ID / Prog IF / Subclass / Class Code",
        0x0C: "Cache Line Size / Latency Timer / Header Type / BIST",
        0x10: "BAR0",
        0x14: "BAR1",
        0x18: "BAR2",
        0x1C: "BAR3",
        0x20: "BAR4",
        0x24: "BAR5",
        0x28: "Cardbus CIS Pointer",
        0x2C: "Subsystem Vendor ID / Subsystem ID",
        0x30: "Expansion ROM Base Address",
        0x34: "Capabilities Pointer",
        0x38: "Reserved",
        0x3C: "Interrupt Line / Interrupt Pin / Min_Gnt / Max_Lat",
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
        board: Optional[str] = None
    ) -> str:
        if len(config_space_data) % 4 != 0:
            raise ValueError(
                "Config space data length must be a multiple of 4 bytes (dword aligned).")
        dwords = self.convert_to_dword_list(config_space_data)
        lines = []
        header_lines = []
        if include_comments:
            if vendor_id:
                header_lines.append(f"// Vendor ID: {vendor_id}")
            if device_id:
                header_lines.append(f"// Device ID: {device_id}")
            if class_code:
                header_lines.append(f"// Class Code: {class_code}")
            if board:
                header_lines.append(f"// Board: {board}")
            if header_lines:
                lines.extend(header_lines)
        for i in range(0, len(dwords), words_per_line):
            line_dwords = dwords[i:i+words_per_line]
            hex_words = ' '.join(f"{dw:08x}" for dw in line_dwords)
            if include_comments:
                offset = i * 4
                comment = self._get_register_comment(offset)
                if comment:
                    lines.append(f"{hex_words} // 0x{offset:02X}: {comment}")
                else:
                    lines.append(f"{hex_words} // 0x{offset:02X}")
            else:
                lines.append(hex_words)
        return '\n'.join(lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        # Only standard PCI config space (first 64 bytes) are commented
        if offset in self._REGISTER_COMMENTS:
            return self._REGISTER_COMMENTS[offset]
        return None

    def write_hex_file(
        self,
        config_space_data: bytes,
        output_path: Union[str, Path],
        include_comments: bool = True
    ) -> Path:
        output_path = Path(output_path)
        hex_str = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments)
        try:
            with output_path.open('w', encoding='utf-8') as f:
                f.write(hex_str)
        except Exception as e:
            raise IOError(f"Failed to write hex file: {e}")
        return output_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        hex_file_path = Path(hex_file_path)
        try:
            with hex_file_path.open('r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('//'):
                        continue
                    # Remove comments
                    if '//' in line:
                        line = line.split('//', 1)[0].strip()
                    if not line:
                        continue
                    # Each word should be 8 hex digits
                    words = line.split()
                    for word in words:
                        if len(word) != 8:
                            return False
                        int(word, 16)  # Will raise ValueError if not hex
            return True
        except Exception:
            return False

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        if len(config_space_data) % 4 != 0:
            raise ValueError(
                "Config space data length must be a multiple of 4 bytes (dword aligned).")
        dwords = []
        for i in range(0, len(config_space_data), 4):
            dword = int.from_bytes(
                config_space_data[i:i+4], byteorder='little')
            dwords.append(dword)
        return dwords
