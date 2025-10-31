
from typing import Optional, Union, List, Path
import os


class ConfigSpaceHexFormatter:

    def __init__(self):
        self.register_comments = {
            0x00: "Vendor ID",
            0x02: "Device ID",
            0x04: "Command",
            0x06: "Status",
            0x08: "Revision ID",
            0x09: "Program Interface",
            0x0A: "Subclass",
            0x0B: "Class Code",
            0x0C: "Cache Line Size",
            0x0D: "Latency Timer",
            0x0E: "Header Type",
            0x0F: "BIST",
            0x10: "Base Address 0",
            0x14: "Base Address 1",
            0x18: "Base Address 2",
            0x1C: "Base Address 3",
            0x20: "Base Address 4",
            0x24: "Base Address 5",
            0x28: "Cardbus CIS Pointer",
            0x2C: "Subsystem Vendor ID",
            0x2E: "Subsystem ID",
            0x30: "Expansion ROM Base Address",
            0x34: "Capabilities Pointer",
            0x38: "Reserved",
            0x3C: "Interrupt Line",
            0x3D: "Interrupt Pin",
            0x3E: "Min Grant",
            0x3F: "Max Latency"
        }

    def format_config_space_to_hex(self, config_space_data: bytes, include_comments: bool = True, words_per_line: int = 1, vendor_id: Optional[str] = None, device_id: Optional[str] = None, class_code: Optional[str] = None, board: Optional[str] = None) -> str:
        lines = []
        for i in range(0, len(config_space_data), 4):
            dword = config_space_data[i:i+4]
            hex_value = dword.hex().upper()
            comment = self._get_register_comment(
                i) if include_comments else None
            line = f"{i:02X}: {hex_value}"
            if comment:
                line += f"  ; {comment}"
            lines.append(line)
        return "\n".join(lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        return self.register_comments.get(offset)

    def write_hex_file(self, config_space_data: bytes, output_path: Union[str, Path], include_comments: bool = True) -> Path:
        hex_content = self.format_config_space_to_hex(
            config_space_data, include_comments)
        if isinstance(output_path, str):
            output_path = Path(output_path)
        with output_path.open('w') as f:
            f.write(hex_content)
        return output_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        if isinstance(hex_file_path, str):
            hex_file_path = Path(hex_file_path)
        if not hex_file_path.exists():
            return False
        with hex_file_path.open('r') as f:
            for line in f:
                parts = line.split(';')
                hex_part = parts[0].strip()
                if not hex_part:
                    continue
                try:
                    offset, hex_value = hex_part.split(':')
                    int(offset, 16)
                    bytes.fromhex(hex_value.strip())
                except ValueError:
                    return False
        return True

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        return [int.from_bytes(config_space_data[i:i+4], byteorder='little') for i in range(0, len(config_space_data), 4)]
