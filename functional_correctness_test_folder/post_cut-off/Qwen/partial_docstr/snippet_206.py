
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
        if len(config_space_data) % 4 != 0:
            raise ValueError(
                "Config space data must be a multiple of 4 bytes.")

        dwords = self.convert_to_dword_list(config_space_data)
        formatted_lines = []
        for i, dword in enumerate(dwords):
            offset = i * 4
            hex_value = f"{dword:08X}"
            comment = self._get_register_comment(
                offset) if include_comments else None
            line = f"{hex_value} // {comment}" if comment else hex_value
            formatted_lines.append(line)
            if (i + 1) % words_per_line == 0:
                formatted_lines.append("")

        return "\n".join(formatted_lines).strip()

    def _get_register_comment(self, offset: int) -> Optional[str]:
        return self.register_comments.get(offset)

    def write_hex_file(self, config_space_data: bytes, output_path: Union[str, Path], include_comments: bool = True) -> Path:
        hex_content = self.format_config_space_to_hex(
            config_space_data, include_comments)
        try:
            with open(output_path, 'w') as f:
                f.write(hex_content)
        except IOError as e:
            raise IOError(f"Failed to write to file {output_path}: {e}")
        return Path(output_path)

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        try:
            with open(hex_file_path, 'r') as f:
                lines = f.readlines()
        except IOError:
            return False

        for line in lines:
            line = line.strip()
            if line and not line.startswith("//"):
                try:
                    int(line.split()[0], 16)
                except ValueError:
                    return False
        return True

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        if len(config_space_data) % 4 != 0:
            raise ValueError(
                "Config space data must be a multiple of 4 bytes.")

        dwords = []
        for i in range(0, len(config_space_data), 4):
            dword = int.from_bytes(
                config_space_data[i:i+4], byteorder='little')
            dwords.append(dword)
        return dwords
