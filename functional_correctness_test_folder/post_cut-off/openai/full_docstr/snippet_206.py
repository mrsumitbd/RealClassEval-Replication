
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional, Union

# Standard PCI configuration space register offsets (in bytes)
PCI_REGISTERS = {
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
    0x38: "Interrupt Line",
    0x39: "Interrupt Pin",
    0x3A: "Min_Gnt",
    0x3B: "Max_Lat",
    # Extended registers (0x40+)
    0x40: "Extended Capabilities Pointer",
    0x44: "MSI/MSI-X Enable",
    0x48: "PCI Express Capabilities",
    0x4C: "PCI Express Device Capabilities",
    0x50: "PCI Express Device Control",
    0x54: "PCI Express Device Status",
    0x58: "PCI Express Link Capabilities",
    0x5C: "PCI Express Link Control",
    0x60: "PCI Express Link Status",
    0x64: "PCI Express Slot Capabilities",
    0x68: "PCI Express Slot Control",
    0x6C: "PCI Express Slot Status",
    0x70: "PCI Express Root Port Capabilities",
    0x74: "PCI Express Root Port Control",
    0x78: "PCI Express Root Port Status",
    0x7C: "PCI Express Root Port Link Capabilities",
    0x80: "PCI Express Root Port Link Control",
    0x84: "PCI Express Root Port Link Status",
    0x88: "PCI Express Root Port Power Management Capabilities",
    0x8C: "PCI Express Root Port Power Management Control",
    0x90: "PCI Express Root Port Power Management Status",
    0x94: "PCI Express Root Port Vendor Specific Capabilities",
    0x98: "PCI Express Root Port Vendor Specific Control",
    0x9C: "PCI Express Root Port Vendor Specific Status",
}


class ConfigSpaceHexFormatter:
    """
    Formats PCI configuration space data into hex files for FPGA initialization.
    """

    def __init__(self):
        """Initialize the hex formatter."""
        # No state needed for now
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
        if not isinstance(config_space_data, (bytes, bytearray)):
            raise ValueError("config_space_data must be bytes or bytearray")

        # Pad to a multiple of 4 bytes
        if len(config_space_data) % 4 != 0:
            padding = 4 - (len(config_space_data) % 4)
            config_space_data += b"\x00" * padding

        dwords = self.convert_to_dword_list(config_space_data)

        lines: List[str] = []

        # Optional header comments
        if include_comments:
            header = []
            if vendor_id:
                header.append(f"// Vendor ID: {vendor_id}")
            if device_id:
                header.append(f"// Device ID: {device_id}")
            if class_code:
                header.append(f"// Class Code: {class_code}")
            if board:
                header.append(f"// Board: {board}")
            if header:
                lines.extend(header)

        # Build hex lines
        for i, dword in enumerate(dwords):
            hex_str = f"{dword:08X}"
            if include_comments:
                offset = i * 4
                comment = self._get_register_comment(offset)
                if comment:
                    hex_str += f" // {comment}"
            lines.append(hex_str)

        # Group words per line
        if words_per_line > 1:
            grouped_lines = []
            for i in range(0, len(lines), words_per_line):
                group = lines[i: i + words_per_line]
                grouped_lines.append(", ".join(group))
            lines = grouped_lines

        return "\n".join(lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        """
        Get a descriptive comment for a register offset.
        """
        return PCI_REGISTERS.get(offset)

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
        except Exception as exc:
            raise IOError(f"Failed to write hex file: {exc}") from exc
        return path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        """
        Validate a hex file for proper formatting.
        """
        path = Path(hex_file_path)
        if not path.is_file():
            return False

        hex_line_re = re.compile(
            r"^\s*([0-9A-Fa-f]{8})(\s*,\s*[0-9A-Fa-f]{8})*\s*(//.*)?$")

        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("//"):
                        continue
                    if not hex_line_re.match(line):
                        return False
            return True
        except Exception:
            return False

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        """
        Convert configuration space bytes to a list of 32-bit dwords.
        """
        if len(config_space_data) % 4 != 0:
            padding = 4 - (len(config_space_data) % 4)
            config_space_data += b"\x00" * padding

        dwords: List[int] = []
        for i in range(0, len(config_space_data), 4):
            chunk = config_space_data[i: i + 4]
            dword = int.from_bytes(chunk, byteorder="little")
            dwords.append(dword)
        return dwords
