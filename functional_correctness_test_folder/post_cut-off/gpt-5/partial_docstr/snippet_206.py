from pathlib import Path
from typing import List, Optional, Union
from datetime import datetime
import re


class ConfigSpaceHexFormatter:

    def __init__(self):
        self._register_map = {
            0x00: "Vendor ID / Device ID",
            0x04: "Command / Status",
            0x08: "Revision ID / Class Code",
            0x0C: "Cache Line Size / Latency Timer / Header Type / BIST",
            0x10: "BAR0",
            0x14: "BAR1",
            0x18: "BAR2",
            0x1C: "BAR3",
            0x20: "BAR4",
            0x24: "BAR5",
            0x28: "CardBus CIS Pointer",
            0x2C: "Subsystem Vendor ID / Subsystem ID",
            0x30: "Expansion ROM Base Address",
            0x34: "Capabilities Pointer",
            0x38: "Reserved",
            0x3C: "Interrupt Line / Interrupt Pin / Min_Gnt / Max_Lat",
        }

    def format_config_space_to_hex(
        self,
        config_space_data: bytes,
        include_comments: bool = True,
        words_per_line: int = 1,
        vendor_id: Optional[str] = None,
        device_id: Optional[str] = None,
        class_code: Optional[str] = None,
        board: Optional[str] = None
    ) -> str:
        '''
        Convert configuration space data to hex format.
        Args:
            config_space_data: Raw configuration space bytes
            include_comments: Whether to include offset/register comments
            words_per_line: Number of 32-bit words per line (default: 1)
        Returns:
            Formatted hex string suitable for $readmemh
        Raises:
            ValueError: If config space data is invalid
        '''
        if not isinstance(config_space_data, (bytes, bytearray)):
            raise ValueError("config_space_data must be bytes or bytearray")
        if len(config_space_data) == 0 or len(config_space_data) % 4 != 0:
            raise ValueError(
                "config_space_data length must be a non-zero multiple of 4 bytes")
        if not isinstance(words_per_line, int) or words_per_line <= 0:
            raise ValueError("words_per_line must be a positive integer")

        dwords = self.convert_to_dword_list(config_space_data)

        lines: List[str] = []
        if include_comments:
            header = []
            header.append("// PCI Configuration Space ($readmemh format)")
            meta_parts = []
            if vendor_id:
                meta_parts.append(f"VendorID={vendor_id}")
            if device_id:
                meta_parts.append(f"DeviceID={device_id}")
            if class_code:
                meta_parts.append(f"ClassCode={class_code}")
            if board:
                meta_parts.append(f"Board={board}")
            if meta_parts:
                header.append("// " + " | ".join(meta_parts))
            header.append(
                f"// Generated: {datetime.now().isoformat(timespec='seconds')}")
            header.append(
                "// Format: 32-bit little-endian DWORDs, hex, space-separated")
            lines.extend(header)

        # Build the hex lines
        per_line_tokens: List[str] = []
        per_line_comments: List[str] = []
        for i, val in enumerate(dwords):
            offset = i * 4
            token = f"{val:08x}"
            per_line_tokens.append(token)

            if include_comments:
                reg_cmt = self._get_register_comment(offset)
                if reg_cmt:
                    per_line_comments.append(f"0x{offset:02x}: {reg_cmt}")
                else:
                    per_line_comments.append(f"0x{offset:02x}")

            if (i + 1) % words_per_line == 0:
                if include_comments:
                    comment = " // " + \
                        "; ".join(
                            per_line_comments) if per_line_comments else ""
                else:
                    comment = ""
                lines.append(" ".join(per_line_tokens) + comment)
                per_line_tokens = []
                per_line_comments = []

        # Flush remaining tokens if not aligned to words_per_line
        if per_line_tokens:
            if include_comments:
                comment = " // " + \
                    "; ".join(per_line_comments) if per_line_comments else ""
            else:
                comment = ""
            lines.append(" ".join(per_line_tokens) + comment)

        return "\n".join(lines)

    def _get_register_comment(self, offset: int) -> Optional[str]:
        '''
        Get a descriptive comment for a register offset.
        Args:
            offset: Register offset in configuration space
        Returns:
            Register description or None if no standard register
        '''
        return self._register_map.get(offset)

    def write_hex_file(self, config_space_data: bytes, output_path: Union[str, Path], include_comments: bool = True) -> Path:
        '''
        Write configuration space data to a hex file.
        Args:
            config_space_data: Raw configuration space bytes
            output_path: Path where hex file should be written
            include_comments: Whether to include offset/register comments
        Returns:
            Path to the written hex file
        Raises:
            IOError: If file cannot be written
        '''
        text = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments)
        out_path = Path(output_path)
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(text, encoding="utf-8", newline="\n")
        except Exception as e:
            raise IOError(f"Failed to write hex file: {e}") from e
        return out_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        path = Path(hex_file_path)
        if not path.is_file():
            return False

        hex_word_re = re.compile(r"^[0-9a-fA-F]{1,8}$")
        has_any = False

        try:
            with path.open("r", encoding="utf-8") as f:
                for raw_line in f:
                    line = raw_line.strip()
                    if not line:
                        continue
                    # Remove comment portion
                    if "//" in line:
                        line = line.split("//", 1)[0].strip()
                    if not line:
                        continue
                    tokens = line.split()
                    for tok in tokens:
                        if not hex_word_re.match(tok):
                            return False
                        has_any = True
        except Exception:
            return False

        return has_any

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        '''
        Convert configuration space bytes to a list of 32-bit dwords.
        Args:
            config_space_data: Raw configuration space bytes
        Returns:
            List of 32-bit integers in little-endian format
        '''
        if not isinstance(config_space_data, (bytes, bytearray)):
            raise ValueError("config_space_data must be bytes or bytearray")
        n = len(config_space_data)
        if n == 0 or n % 4 != 0:
            raise ValueError(
                "config_space_data length must be a non-zero multiple of 4 bytes")
        return [int.from_bytes(config_space_data[i:i+4], "little") for i in range(0, n, 4)]
