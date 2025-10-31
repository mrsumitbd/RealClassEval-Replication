
from pathlib import Path
from typing import Optional, Union, List


class ConfigSpaceHexFormatter:

    def __init__(self):
        pass

    def format_config_space_to_hex(self, config_space_data: bytes, include_comments: bool = True, words_per_line: int = 1, vendor_id: Optional[str] = None, device_id: Optional[str] = None, class_code: Optional[str] = None, board: Optional[str] = None) -> str:
        if len(config_space_data) % 4 != 0:
            raise ValueError(
                "Configuration space data length must be a multiple of 4 bytes")

        dword_list = self.convert_to_dword_list(config_space_data)
        hex_lines = []
        for i, dword in enumerate(dword_list):
            offset = i * 4
            hex_line = f"@{offset:04X} {dword:08X}"
            if include_comments:
                comment = self._get_register_comment(offset)
                if comment:
                    hex_line += f" // {comment}"
            hex_lines.append(hex_line)

        formatted_hex = "\n".join(hex_lines)
        return formatted_hex

    def _get_register_comment(self, offset: int) -> Optional[str]:
        register_comments = {
            0x00: "Vendor ID",
            0x02: "Device ID",
            0x04: "Command Register",
            0x06: "Status Register",
            0x08: "Revision ID",
            0x09: "Class Code",
            0x0A: "Cache Line Size",
            0x0C: "Latency Timer",
            0x0D: "Header Type",
            0x0E: "BIST",
            0x10: "Base Address Register 0",
            0x14: "Base Address Register 1",
            0x18: "Base Address Register 2",
            0x1C: "Base Address Register 3",
            0x20: "Base Address Register 4",
            0x24: "Base Address Register 5",
            0x28: "CardBus CIS Pointer",
            0x2C: "Subsystem Vendor ID",
            0x2E: "Subsystem Device ID",
            0x30: "Expansion ROM Base Address",
            0x3C: "Interrupt Line",
            0x3D: "Interrupt Pin",
            0x3E: "Minimum Grant",
            0x3F: "Maximum Latency"
        }
        return register_comments.get(offset, None)

    def write_hex_file(self, config_space_data: bytes, output_path: Union[str, Path], include_comments: bool = True) -> Path:
        formatted_hex = self.format_config_space_to_hex(
            config_space_data, include_comments)
        output_path = Path(output_path)
        output_path.write_text(formatted_hex)
        return output_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        hex_file_path = Path(hex_file_path)
        if not hex_file_path.exists():
            return False

        try:
            with open(hex_file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if not line.startswith('@'):
                        return False
                    parts = line.split()
                    if len(parts) < 2:
                        return False
                    try:
                        int(parts[0][1:], 16)
                        int(parts[1], 16)
                    except ValueError:
                        return False
        except IOError:
            return False

        return True

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        dword_list = []
        for i in range(0, len(config_space_data), 4):
            dword_bytes = config_space_data[i:i+4]
            dword = int.from_bytes(dword_bytes, byteorder='little')
            dword_list.append(dword)
        return dword_list
