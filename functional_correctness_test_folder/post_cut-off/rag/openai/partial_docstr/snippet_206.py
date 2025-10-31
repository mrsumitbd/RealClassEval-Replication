
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional, Union

# --------------------------------------------------------------------------- #
# ConfigSpaceHexFormatter
# --------------------------------------------------------------------------- #


class ConfigSpaceHexFormatter:
    """
    Formats PCI configuration space data into hex files for FPGA initialization.
    This class handles:
    - Converting configuration space bytes to little-endian 32‑bit words
    - Generating properly formatted hex files for Vivado $readmemh
    - Adding debug comments with register offsets
    - Ensuring proper alignment and padding
    """

    # Standard PCI configuration register offsets (in bytes)
    _REGISTER_MAP = {
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
    }

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
            words_per_line: Number of 32‑bit words per line (default: 1)
            vendor_id: Optional vendor ID string (e.g. "0x1234")
            device_id: Optional device ID string (e.g. "0x5678")
            class_code: Optional class code string
            board: Optional board name

        Returns:
            Formatted hex string suitable for $readmemh

        Raises:
            ValueError: If config space data is invalid
        """
        if not isinstance(config_space_data, (bytes, bytearray)):
            raise ValueError("config_space_data must be bytes or bytearray")

        # Pad to a multiple of 4 bytes
        padded = config_space_data
        if len(padded) % 4 != 0:
            padded = padded + b"\x00" * (4 - (len(padded) % 4))

        dwords = self.convert_to_dword_list(padded)

        lines: List[str] = []

        # Optional header comment
        if include_comments:
            header_parts = ["# PCI Configuration Space"]
            if vendor_id:
                header_parts.append(f"Vendor ID: {vendor_id}")
            if device_id:
                header_parts.append(f"Device ID: {device_id}")
            if class_code:
                header_parts.append(f"Class Code: {class_code}")
            if board:
                header_parts.append(f"Board: {board}")
            lines.append("# " + " | ".join(header_parts))

        # Build lines
        for i, dword in enumerate(dwords):
            offset = i * 4
            hex_str = f"{dword:08X}"
            if include_comments:
                comment = self._get_register_comment(offset)
                if comment:
                    hex_str += f"  // {comment}"
                else:
                    hex_str += f"  // 0x{offset:02X}"
            lines.append(hex_str)

        # Group words per line
        if words_per_line > 1:
            grouped_lines: List[str] = []
            for i in range(0, len(lines), words_per_line):
                grouped_lines.append(" ".join(lines[i: i + words_per_line]))
            return "\n".join(grouped_lines)
        else:
            return "\n".join(lines)

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
        path = Path(output_path).expanduser().resolve()
        hex_str = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments
        )
        try:
            path.write_text(hex_str, encoding="utf-8")
        except OSError as exc:
            raise IOError(f"Failed to write hex file {path}: {exc}") from exc
        return path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        """
        Validate a hex file for proper formatting.

        Args:
            hex_file_path: Path to hex file to validate

        Returns:
            True if valid, False otherwise
        """
        path = Path(hex_file_path).expanduser().resolve()
        if not path.is_file():
            return False

        try:
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Remove comments
                    if "//" in line:
                        line = line.split("//", 1)[0].strip()
                    if not line:
                        continue
                    # Split by whitespace
                    tokens = line.split()
                    for token in tokens:
                        if len(token) != 8:
                            return False
                        try:
                            int(token, 16)
                        except ValueError:
                            return False
            return True
        except Exception:
            return False

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        """
        Convert configuration space bytes to a list of 32‑bit dwords.

        Args:
            config_space_data: Raw configuration space bytes

        Returns:
            List of 32‑bit integers in little‑endian format
        """
        if not isinstance(config_space_data, (bytes, bytearray)):
            raise ValueError("config_space_data must be bytes or bytearray")

        # Pad to a multiple of 4 bytes
        padded = config_space_data
        if len(padded) % 4 != 0:
            padded = padded + b"\x00"
