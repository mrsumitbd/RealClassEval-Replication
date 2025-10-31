
from typing import Optional, Union, List
from pathlib import Path


class ConfigSpaceHexFormatter:

    def __init__(self):
        self.register_comments = {
            0x00: "Vendor ID",
            0x02: "Device ID",
            0x04: "Command",
            0x06: "Status",
            0x08: "Revision ID",
            0x09: "Class Code",
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
            0x28: "CardBus CIS Pointer",
            0x2C: "Subsystem Vendor ID",
            0x2E: "Subsystem ID",
            0x30: "Expansion ROM Base Address",
            0x34: "Capabilities Pointer",
            0x3C: "Interrupt Line",
            0x3D: "Interrupt Pin",
            0x3E: "Min_Gnt",
            0x3F: "Max_Lat"
        }

    def format_config_space_to_hex(self, config_space_data: bytes, include_comments: bool = True, words_per_line: int = 1, vendor_id: Optional[str] = None, device_id: Optional[str] = None, class_code: Optional[str] = None, board: Optional[str] = None) -> str:
        if len(config_space_data) % 4 != 0:
            raise ValueError("Config space data must be a multiple of 4 bytes")

        dword_list = self.convert_to_dword_list(config_space_data)
        hex_lines = []
        for i, dword in enumerate(dword_list):
            hex_line = f"{dword:08x}"
            if include_comments:
                comment = self._get_register_comment(i * 4)
                if comment:
                    hex_line += f" // {comment}"
                else:
                    hex_line += f" // Offset {i * 4:02x}"
            hex_lines.append(hex_line)

        formatted_hex = "\n".join([", ".join(hex_lines[i:i+words_per_line])
                                  for i in range(0, len(hex_lines), words_per_line)])

        if vendor_id and device_id and class_code and board:
            header = f"// Vendor ID: {vendor_id}, Device ID: {device_id}, Class Code: {class_code}, Board: {board}\n"
            formatted_hex = header + formatted_hex

        return formatted_hex

    def _get_register_comment(self, offset: int) -> Optional[str]:
        return self.register_comments.get(offset)

    def write_hex_file(self, config_space_data: bytes, output_path: Union[str, Path], include_comments: bool = True) -> Path:
        output_path = Path(output_path)
        try:
            with open(output_path, 'w') as f:
                f.write(self.format_config_space_to_hex(
                    config_space_data, include_comments))
            return output_path
        except IOError as e:
            raise IOError(f"Failed to write hex file: {e}")

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        try:
            with open(hex_file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("//"):
                        continue
                    if not line:
                        continue
                    values = line.split(",")
                    for value in values:
                        value = value.strip()
                        if not value:
                            continue
                        try:
                            int(value, 16)
                        except ValueError:
                            return False
            return True
        except IOError:
            return False

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        return [int.from_bytes(config_space_data[i:i+4], 'little') for i in range(0, len(config_space_data), 4)]
