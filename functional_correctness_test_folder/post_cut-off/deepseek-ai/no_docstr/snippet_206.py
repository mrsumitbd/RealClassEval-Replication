
from typing import Optional, Union, List
from pathlib import Path


class ConfigSpaceHexFormatter:

    def __init__(self):
        pass

    def format_config_space_to_hex(self, config_space_data: bytes, include_comments: bool = True, words_per_line: int = 1, vendor_id: Optional[str] = None, device_id: Optional[str] = None, class_code: Optional[str] = None, board: Optional[str] = None) -> str:
        hex_lines = []
        dwords = self.convert_to_dword_list(config_space_data)

        for i, dword in enumerate(dwords):
            offset = i * 4
            hex_str = f"{dword:08X}"
            line = hex_str

            if include_comments:
                comment = self._get_register_comment(offset)
                if comment:
                    line += f" // {comment}"

            hex_lines.append(line)

        return '\n'.join(hex_lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        comments = {
            0x00: "Vendor ID",
            0x04: "Device ID",
            0x08: "Command",
            0x0C: "Status",
            0x10: "Revision ID",
            0x2C: "Subsystem Vendor ID",
            0x30: "Subsystem ID",
        }
        return comments.get(offset)

    def write_hex_file(self, config_space_data: bytes, output_path: Union[str, Path], include_comments: bool = True) -> Path:
        hex_content = self.format_config_space_to_hex(
            config_space_data, include_comments)
        output_path = Path(output_path)
        output_path.write_text(hex_content)
        return output_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        try:
            hex_file_path = Path(hex_file_path)
            content = hex_file_path.read_text().splitlines()
            for line in content:
                if '//' in line:
                    line = line.split('//')[0].strip()
                if not line:
                    continue
                int(line, 16)
            return True
        except (ValueError, FileNotFoundError):
            return False

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        dwords = []
        for i in range(0, len(config_space_data), 4):
            chunk = config_space_data[i:i+4]
            dword = int.from_bytes(chunk, byteorder='little')
            dwords.append(dword)
        return dwords
