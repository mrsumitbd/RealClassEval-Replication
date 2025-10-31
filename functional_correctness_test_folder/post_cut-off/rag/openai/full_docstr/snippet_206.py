
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional, Union

# --------------------------------------------------------------------------- #
#  ConfigSpaceHexFormatter
# --------------------------------------------------------------------------- #


class ConfigSpaceHexFormatter:
    """
    Formats PCI configuration space data into hex files for FPGA initialization.
    This class handles:
    - Converting configuration space bytes to little‑endian 32‑bit words
    - Generating properly formatted hex files for Vivado $readmemh
    - Adding debug comments with register offsets
    - Ensuring proper alignment and padding
    """

    # Standard PCI configuration space register names (offset → description)
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
        0x3C: "Reserved",
        0x3D: "Reserved",
        0x3E: "Reserved",
        0x3F: "Reserved",
    }

    def __init__(self) -> None:
        """Initialize the hex formatter."""
        # Nothing special to initialise at the moment
        pass

    # --------------------------------------------------------------------- #
    #  Public API
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
            vendor_id: Optional vendor ID string (ignored in formatting)
            device_id: Optional device ID string (ignored in formatting)
            class_code: Optional class code string (ignored in formatting)
            board: Optional board string (ignored in formatting)

        Returns:
            Formatted hex string suitable for $readmemh

        Raises:
            ValueError: If config space data is invalid
        """
        if not isinstance(config_space_data, (bytes, bytearray)):
            raise ValueError("config_space_data must be bytes or bytearray")

        if len(config_space_data) == 0:
            raise ValueError("config_space_data is empty")

        # Pad to a multiple of 4 bytes if necessary
        if len(config_space_data) % 4 != 0:
            padding = 4 - (len(config_space_data) % 4)
            config_space_data += b"\x00" * padding

        dwords = self.convert_to_dword_list(config_space_data)

        lines: List[str] = []
        for i in range(0, len(dwords), words_per_line):
            chunk = dwords[i: i + words_per_line]
            hex_values = [f"{dw:08X}" for dw in chunk]
            line = ", ".join(hex_values)
            if include_comments:
                offset = i * 4
                comment = self._get_register_comment(offset)
                if comment:
                    line += f" // {comment}"
            lines.append(line)

        return "\n".join(lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        """
        Get a descriptive comment for a register offset.

        Args:
            offset: Register offset in configuration space

        Returns:
            Register description or None if no standard register
        """
        return self._REGISTER_MAP.get(offset)

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
        path = Path(output_path)
        hex_str = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments
        )
        try:
            path.write_text(hex_str, encoding="utf-8")
        except OSError as exc:
            raise IOError(f"Failed to write hex file {path!s}: {exc}") from exc
        return path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        """
        Validate a hex file for proper formatting.

        Args:
            hex_file_path: Path to hex file to validate

        Returns:
            True if valid, False otherwise
        """
        path = Path(hex_file_path)
        if not path.is_file():
            return False

        hex_token_re = re.compile(r"^[0-9a-fA-F]{1,8}$")
        try:
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    # Strip comments
                    line = line.split("//", 1)[0].strip()
                    if not line:
                        continue
                    # Split by commas or whitespace
                    tokens = re.split(r"[,\s]+", line)
                    for token in tokens:
                        if not token:
                            continue
                        if not hex_token_re.match(token):
                            return False
            return True
        except OSError:
            return False

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        """
        Convert configuration space bytes to a list of 32‑bit dwords.

        Args:
            config_space_data: Raw configuration space bytes

        Returns:
            List of 32‑bit integers in little‑endian format
        """
        if len(config_space_data) % 4 != 0:
            # Pad with zeros to make a full dword
            padding = 4 - (len(config_space_data) % 4)
            config_space_data += b"\x00" * padding

        dwords: List[int] = []
        for i in range(0, len(config_space_data
