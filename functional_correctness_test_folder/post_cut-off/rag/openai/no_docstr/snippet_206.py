
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional, Union

# --------------------------------------------------------------------------- #
# Helper constants
# --------------------------------------------------------------------------- #

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
    0x38: "Interrupt Line",
    0x39: "Interrupt Pin",
    0x3A: "Min. Latency",
    0x3B: "Max. Latency",
    0x3C: "Cache Line Size (PCIe)",
    0x3D: "Latency Timer (PCIe)",
    0x3E: "Header Type (PCIe)",
    0x3F: "BIST (PCIe)",
}

# --------------------------------------------------------------------------- #
# Main class
# --------------------------------------------------------------------------- #


class ConfigSpaceHexFormatter:
    """
    Formats PCI configuration space data into hex files for FPGA initialization.
    """

    def __init__(self) -> None:
        """Initialize the hex formatter."""
        # No state needed for now
        pass

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #

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

        Args:
            config_space_data: Raw configuration space bytes
            include_comments: Whether to include offset/register comments
            words_per_line: Number of 32-bit words per line (default: 1)
            vendor_id: Optional vendor ID string (e.g., "0x1234")
            device_id: Optional device ID string (e.g., "0x5678")
            class_code: Optional class code string (e.g., "0x01")
            board: Optional board name string

        Returns:
            Formatted hex string suitable for $readmemh

        Raises:
            ValueError: If config space data is invalid
        """
        if not isinstance(config_space_data, (bytes, bytearray)):
            raise ValueError("config_space_data must be bytes or bytearray")

        # Pad to a multiple of 4 bytes
        if len(config_space_data) % 4 != 0:
            padding = 4 - (len(config_space_data) % 4)
            config_space_data += b"\x00" * padding

        dwords = self.convert_to_dword_list(config_space_data)

        lines: List[str] = []

        # Header comments
        if vendor_id or device_id or class_code or board:
            header = "// Configuration Space Hex Dump"
            lines.append(header)
            if vendor_id:
                lines.append(f"// Vendor ID: {vendor_id}")
            if device_id:
                lines.append(f"// Device ID: {device_id}")
            if class_code:
                lines.append(f"// Class Code: {class_code}")
            if board:
                lines.append(f"// Board: {board}")
            lines.append("")  # blank line

        # Build lines
        for idx, dword in enumerate(dwords):
            offset = idx * 4
            hex_word = f"{dword:08x}"
            line = hex_word

            if include_comments:
                comment = self._get_register_comment(offset)
                if comment:
                    line += f" // {comment}"
                else:
                    # If no known register, still show offset
                    line += f" // 0x{offset:02x}"

            lines.append(line)

            # Insert line breaks after words_per_line words
            if words_per_line > 1:
                # Group words_per_line words into a single line
                # We will rebuild lines after grouping
                pass

        # If words_per_line > 1, regroup lines
        if words_per_line > 1:
            grouped_lines: List[str] = []
            for i in range(0, len(lines), words_per_line):
                grouped_lines.append(" ".join(lines[i: i + words_per_line]))
            lines = grouped_lines

        return "\n".join(lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        """
        Get a descriptive comment for a register offset.

        Args:
            offset: Register offset in configuration space

        Returns:
            Register description or None if no standard register
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

        Args:
            config_space_data: Raw configuration space bytes
            output_path: Path where hex file should be written
            include_comments: Whether to include offset/register comments

        Returns:
            Path to the written hex file

        Raises:
            IOError: If file cannot be written
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        hex_str = self.format_config_space_to_hex
