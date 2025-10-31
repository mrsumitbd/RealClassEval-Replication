
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Union


class ConfigSpaceHexFormatter:
    """
    Utility class for formatting PCI configuration space data into a human‑readable
    hexadecimal representation, writing it to a file, validating the file, and
    converting the raw bytes into a list of 32‑bit words.
    """

    # Mapping of register offsets to human‑readable comments
    _REGISTER_COMMENTS = {
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
        0x30: "Subsystem ID",
        0x34: "Expansion ROM Base Address",
        0x38: "Capabilities Pointer",
        0x3C: "Interrupt Line",
    }

    def __init__(self) -> None:
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
        Convert a 256‑byte configuration space into a formatted hex string.

        Parameters
        ----------
        config_space_data : bytes
            Raw configuration space data (up to 256 bytes). Shorter data is padded with zeros.
        include_comments : bool, optional
            If True, include register comments where known.
        words_per_line : int, optional
            Number of 16‑bit words per line.
        vendor_id, device_id, class_code, board : Optional[str]
            Optional header information to prepend as comments.

        Returns
        -------
        str
            Formatted hex representation.
        """
        # Ensure we have exactly 256 bytes
        data = config_space_data.ljust(256, b"\x00")

        lines: List[str] = []

        # Optional header comments
        if vendor_id or device_id or class_code or board:
            header = []
            if vendor_id:
                header.append(f"Vendor ID: {vendor_id}")
            if device_id:
                header.append(f"Device ID: {device_id}")
            if class_code:
                header.append(f"Class Code: {class_code}")
            if board:
                header.append(f"Board: {board}")
            lines.append("; " + " | ".join(header))

        # Process words
        for offset in range(0, 256, 2):
            word_bytes = data[offset: offset + 2]
            word_value = int.from_bytes(word_bytes, "little")
            hex_word = f"0x{word_value:04X}"
            comment = ""
            if include_comments:
                reg_comment = self._get_register_comment(offset)
                if reg_comment:
                    comment = f" ; {reg_comment}"
            # Append to current line
            if len(lines) == 0 or len(lines[-1].split()) >= words_per_line:
                lines.append(hex_word + comment)
            else:
                lines[-1] += " " + hex_word + comment

        return "\n".join(lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        """
        Return a comment string for a given register offset, if known.
        """
        return self._REGISTER_COMMENTS.get(offset)

    def write_hex_file(
        self,
        config_space_data: bytes,
        output_path: Union[str, Path],
        include_comments: bool = True,
    ) -> Path:
        """
        Write the formatted hex representation to a file.

        Parameters
        ----------
        config_space_data : bytes
            Raw configuration space data.
        output_path : Union[str, Path]
            Destination file path.
        include_comments : bool, optional
            Whether to include register comments.

        Returns
        -------
        Path
            Path object pointing to the written file.
        """
        path = Path(output_path)
        hex_text = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments
        )
        path.write_text(hex_text, encoding="utf-8")
        return path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        """
        Validate that a hex file contains exactly 128 16‑bit words,
        each formatted as 0xHHHH, optionally followed by a comment.

        Parameters
        ----------
        hex_file_path : Union[str, Path]
            Path to the hex file.

        Returns
        -------
        bool
            True if the file is valid, False otherwise.
        """
        path = Path(hex_file_path)
        if not path.is_file():
            return False

        word_count = 0
        for line in path.read_text(encoding="utf-8").splitlines():
            # Skip empty lines and comment‑only lines
            stripped = line.strip()
            if not stripped or stripped.startswith(";"):
                continue
            # Remove comment part
            if ";" in stripped:
                stripped = stripped.split(";", 1)[0].strip()
            # Split into words
            for token in stripped.split():
                if not token.startswith("0x") or len(token) != 6:
                    return False
                try:
                    int(token, 16)
                except ValueError:
                    return False
                word_count += 1

        return word_count == 128

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        """
        Convert the raw configuration space bytes into a list of 32‑bit little‑endian words.

        Parameters
        ----------
        config_space_data : bytes
            Raw configuration space data (up to 256 bytes).

        Returns
        -------
        List[int]
            List of 32‑bit integers.
        """
        data = config_space_data.ljust(256, b"\x00")
        dwords: List[int] = []
        for offset in range(0, 256, 4):
            dword_bytes = data[offset: offset + 4]
            dword = int.from_bytes(dword_bytes, "little")
            dwords.append(dword)
        return dwords
