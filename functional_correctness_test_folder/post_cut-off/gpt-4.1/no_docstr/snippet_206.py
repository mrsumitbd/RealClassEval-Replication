
from typing import Optional, Union, List
from pathlib import Path


class ConfigSpaceHexFormatter:

    # PCI config space register names for comments (offset: name)
    _register_comments = {
        0x00: "Vendor ID",
        0x02: "Device ID",
        0x04: "Command",
        0x06: "Status",
        0x08: "Revision ID",
        0x09: "Prog IF",
        0x0A: "Subclass",
        0x0B: "Class Code",
        0x0C: "Cache Line Size",
        0x0D: "Latency Timer",
        0x0E: "Header Type",
        0x0F: "BIST",
        # ... more can be added as needed
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
        lines = []
        if include_comments:
            lines.append("# PCI Config Space Hex Dump")
            if vendor_id:
                lines.append(f"# Vendor ID: {vendor_id}")
            if device_id:
                lines.append(f"# Device ID: {device_id}")
            if class_code:
                lines.append(f"# Class Code: {class_code}")
            if board:
                lines.append(f"# Board: {board}")
            lines.append("# Format: <offset>: <hex dword(s)> [# comment]")

        dword_list = self.convert_to_dword_list(config_space_data)
        total_dwords = len(dword_list)
        for i in range(0, total_dwords, words_per_line):
            offset = i * 4
            dwords = dword_list[i:i+words_per_line]
            hex_words = " ".join(f"{w:08X}" for w in dwords)
            line = f"{offset:03X}: {hex_words}"
            if include_comments:
                comments = []
                for j in range(words_per_line):
                    reg_comment = self._get_register_comment(offset + j*4)
                    if reg_comment:
                        comments.append(reg_comment)
                if comments:
                    line += "    # " + ", ".join(comments)
            lines.append(line)
        return "\n".join(lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        return self._register_comments.get(offset)

    def write_hex_file(
        self,
        config_space_data: bytes,
        output_path: Union[str, Path],
        include_comments: bool = True
    ) -> Path:
        output_path = Path(output_path)
        hex_str = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments)
        output_path.write_text(hex_str)
        return output_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        hex_file_path = Path(hex_file_path)
        try:
            with hex_file_path.open("r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if ':' not in line:
                        return False
                    offset_part, rest = line.split(':', 1)
                    offset_part = offset_part.strip()
                    try:
                        int(offset_part, 16)
                    except ValueError:
                        return False
                    hex_part = rest.strip().split('#')[0].strip()
                    if not hex_part:
                        continue
                    for word in hex_part.split():
                        if len(word) != 8:
                            return False
                        int(word, 16)
            return True
        except Exception:
            return False

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        dword_list = []
        data = config_space_data
        # Pad to multiple of 4 bytes
        if len(data) % 4 != 0:
            data += b'\x00' * (4 - (len(data) % 4))
        for i in range(0, len(data), 4):
            dword = int.from_bytes(data[i:i+4], byteorder='little')
            dword_list.append(dword)
        return dword_list
