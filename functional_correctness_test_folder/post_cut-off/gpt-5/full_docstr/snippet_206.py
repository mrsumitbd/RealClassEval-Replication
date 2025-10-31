from pathlib import Path
from typing import List, Optional, Union


class ConfigSpaceHexFormatter:
    '''
    Formats PCI configuration space data into hex files for FPGA initialization.
    This class handles:
    - Converting configuration space bytes to little-endian 32-bit words
    - Generating properly formatted hex files for Vivado $readmemh
    - Adding debug comments with register offsets
    - Ensuring proper alignment and padding
    '''

    def __init__(self):
        '''Initialize the hex formatter.'''
        # Predefined register descriptions for standard PCI config space offsets
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
        board: Optional[str] = None,
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
            raise ValueError("config_space_data must be bytes-like")
        if words_per_line < 1:
            raise ValueError("words_per_line must be >= 1")

        dwords = self.convert_to_dword_list(config_space_data)

        lines: List[str] = []
        if include_comments:
            header_items = []
            if vendor_id is not None:
                header_items.append(f"VendorID={vendor_id}")
            if device_id is not None:
                header_items.append(f"DeviceID={device_id}")
            if class_code is not None:
                header_items.append(f"ClassCode={class_code}")
            if board is not None:
                header_items.append(f"Board={board}")
            if header_items:
                lines.append("// " + " | ".join(header_items))
            lines.append("// Format: little-endian 32-bit words for $readmemh")
            lines.append(
                "// Offsets shown are byte offsets within PCI config space")

        # Build lines with the requested words_per_line
        for i in range(0, len(dwords), words_per_line):
            group = dwords[i:i + words_per_line]
            tokens = [f"{val:08x}" for val in group]
            line = " ".join(tokens)
            if include_comments:
                # Build per-word offset comments
                comments = []
                for j, _ in enumerate(group):
                    offset = (i + j) * 4
                    reg_desc = self._get_register_comment(offset)
                    if reg_desc:
                        comments.append(f"[0x{offset:03x}]={reg_desc}")
                    else:
                        comments.append(f"[0x{offset:03x}]")
                if comments:
                    line += "   // " + " ".join(comments)
            lines.append(line)

        return "\n".join(lines) + ("\n" if lines else "")

    def _get_register_comment(self, offset: int) -> Optional[str]:
        '''
        Get a descriptive comment for a register offset.
        Args:
            offset: Register offset in configuration space
        Returns:
            Register description or None if no standard register
        '''
        # Direct match
        if offset in self._register_map:
            return self._register_map[offset]
        # BAR region check
        if 0x10 <= offset <= 0x24 and (offset % 4 == 0):
            bar_index = (offset - 0x10) // 4
            return f"BAR{bar_index}"
        return None

    def write_hex_file(
        self,
        config_space_data: bytes,
        output_path: Union[str, Path],
        include_comments: bool = True,
    ) -> Path:
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
        hex_str = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments)
        out_path = Path(output_path)
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(hex_str, encoding="utf-8")
        except Exception as e:
            raise IOError(f"Failed to write hex file: {e}") from e
        return out_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        '''
        Validate a hex file for proper formatting.
        Args:
            hex_file_path: Path to hex file to validate
        Returns:
            True if valid, False otherwise
        '''
        path = Path(hex_file_path)
        if not path.is_file():
            return False
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            return False

        found_data = False
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("//"):
                continue
            # Strip inline comment
            if "//" in line:
                line = line.split("//", 1)[0].rstrip()
            if not line:
                continue
            tokens = line.split()
            if not tokens:
                continue
            found_data = True
            for tok in tokens:
                # Each token must be 1 to 8 hex digits
                if not (1 <= len(tok) <= 8):
                    return False
                try:
                    int(tok, 16)
                except ValueError:
                    return False
        return found_data

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        '''
        Convert configuration space bytes to a list of 32-bit dwords.
        Args:
            config_space_data: Raw configuration space bytes
        Returns:
            List of 32-bit integers in little-endian format
        '''
        if not isinstance(config_space_data, (bytes, bytearray)):
            raise ValueError("config_space_data must be bytes-like")

        data = bytes(config_space_data)
        if len(data) == 0:
            return []

        # Pad to multiple of 4 bytes
        pad = (-len(data)) % 4
        if pad:
            data += b"\x00" * pad

        dwords: List[int] = []
        for i in range(0, len(data), 4):
            dword = int.from_bytes(
                data[i:i + 4], byteorder="little", signed=False)
            dwords.append(dword)
        return dwords
