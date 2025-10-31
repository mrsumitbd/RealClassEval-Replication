
import struct
from pathlib import Path
from typing import List, Optional, Union


class ConfigSpaceHexFormatter:

    def __init__(self):
        pass

    def format_config_space_to_hex(self, config_space_data: bytes, include_comments: bool = True, words_per_line: int = 1, vendor_id: Optional[str] = None, device_id: Optional[str] = None, class_code: Optional[str] = None, board: Optional[str] = None) -> str:
        hex_lines = []
        dword_list = self.convert_to_dword_list(config_space_data)

        for i, dword in enumerate(dword_list):
            offset = i * 4
            hex_line = f":04{offset:04X}00{dword:08X}{self._calculate_checksum(offset, dword):02X}"
            if include_comments:
                comment = self._get_register_comment(offset)
                if comment:
                    hex_line += f" {comment}"
            hex_lines.append(hex_line)

        if vendor_id or device_id or class_code or board:
            hex_lines.append(f"; Vendor ID: {vendor_id or 'N/A'}")
            hex_lines.append(f"; Device ID: {device_id or 'N/A'}")
            hex_lines.append(f"; Class Code: {class_code or 'N/A'}")
            hex_lines.append(f"; Board: {board or 'N/A'}")

        return "\n".join(hex_lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        register_comments = {
            0x00: "Vendor ID",
            0x02: "Device ID",
            0x04: "Command",
            0x06: "Status",
            0x08: "Revision ID",
            0x09: "Class Code",
            0x0C: "Cache Line Size",
            0x0D: "Latency Timer",
            0x0E: "Header Type",
            0x10: "BIST",
            0x14: "Base Address Register 0",
            0x18: "Base Address Register 1",
            0x1C: "Base Address Register 2",
            0x20: "Base Address Register 3",
            0x24: "Base Address Register 4",
            0x28: "Base Address Register 5",
            0x2C: "Cardbus CIS Pointer",
            0x30: "Subsystem Vendor ID",
            0x32: "Subsystem ID",
            0x34: "Expansion ROM Base Address",
            0x3C: "Interrupt Line",
            0x3D: "Interrupt Pin",
            0x3E: "Minimum Grant",
            0x3F: "Maximum Latency"
        }
        return register_comments.get(offset, None)

    def write_hex_file(self, config_space_data: bytes, output_path: Union[str, Path], include_comments: bool = True) -> Path:
        hex_content = self.format_config_space_to_hex(
            config_space_data, include_comments)
        output_path = Path(output_path)
        output_path.write_text(hex_content)
        return output_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        hex_file_path = Path(hex_file_path)
        if not hex_file_path.exists():
            return False

        with hex_file_path.open('r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(';'):
                    continue
                if not self._validate_hex_line(line):
                    return False
        return True

    def _validate_hex_line(self, line: str) -> bool:
        if not line.startswith(':'):
            return False

        byte_count = int(line[1:3], 16)
        address = int(line[3:7], 16)
        record_type = int(line[7:9], 16)
        data = line[9:-2]
        checksum = int(line[-2:], 16)

        if len(data) != byte_count * 2:
            return False

        calculated_checksum = self._calculate_checksum(
            address, int(data, 16), record_type)
        if calculated_checksum != checksum:
            return False

        return True

    def _calculate_checksum(self, address: int, data: int, record_type: int = 0) -> int:
        byte_count = 4
        checksum = byte_count + (address >> 8) + (address & 0xFF) + record_type + (
            data >> 24) + ((data >> 16) & 0xFF) + ((data >> 8) & 0xFF) + (data & 0xFF)
        checksum = (checksum & 0xFF) ^ 0xFF
        checksum += 1
        return checksum & 0xFF

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        dword_list = []
        for i in range(0, len(config_space_data), 4):
            dword = struct.unpack('<I', config_space_data[i:i+4])[0]
            dword_list.append(dword)
        return dword_list
