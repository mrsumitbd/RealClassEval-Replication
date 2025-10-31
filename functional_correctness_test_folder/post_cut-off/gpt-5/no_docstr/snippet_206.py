from pathlib import Path
from typing import List, Optional, Union
import re
from datetime import datetime


class ConfigSpaceHexFormatter:

    def __init__(self):
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
        if words_per_line <= 0:
            raise ValueError("words_per_line must be >= 1")

        dwords = self.convert_to_dword_list(config_space_data)
        if not dwords:
            return ""

        lines: List[str] = []

        if include_comments:
            header = ["# PCI Configuration Space Hex Dump"]
            meta = []
            if vendor_id is not None:
                meta.append(f"Vendor ID: {vendor_id}")
            if device_id is not None:
                meta.append(f"Device ID: {device_id}")
            if class_code is not None:
                meta.append(f"Class Code: {class_code}")
            if board is not None:
                meta.append(f"Board: {board}")
            if meta:
                header.append("# " + ", ".join(meta))
            header.append("# Generated: " +
                          datetime.utcnow().isoformat() + "Z")
            header.append(
                "# Format: 8-hex-digit DWORDs, little-endian order on input")
            lines.extend(header)

        for i in range(0, len(dwords), words_per_line):
            group = dwords[i: i + words_per_line]
            tokens = [f"{val:08X}" for val in group]
            line = " ".join(tokens)
            if include_comments:
                offset = i * 4
                comment = self._get_register_comment(offset)
                base_comment = f"# {offset:03X}h"
                if comment:
                    base_comment += f" - {comment}"
                line = f"{line}  {base_comment}"
            lines.append(line)

        return "\n".join(lines) + "\n"

    def _get_register_comment(self, offset: int) -> Optional[str]:
        comments = {
            0x00: "Vendor ID (15:0), Device ID (31:16)",
            0x04: "Command (15:0), Status (31:16)",
            0x08: "Revision ID, Prog IF, Subclass, Class Code",
            0x0C: "Cache Line Size, Latency Timer, Header Type, BIST",
            0x10: "BAR0",
            0x14: "BAR1",
            0x18: "BAR2",
            0x1C: "BAR3",
            0x20: "BAR4",
            0x24: "BAR5",
            0x28: "CardBus CIS Pointer",
            0x2C: "Subsystem Vendor ID, Subsystem ID",
            0x30: "Expansion ROM Base Address",
            0x34: "Capabilities Pointer",
            0x38: "Reserved",
            0x3C: "Interrupt Line, Interrupt Pin, Min_Gnt, Max_Lat",
        }
        return comments.get(offset)

    def write_hex_file(
        self,
        config_space_data: bytes,
        output_path: Union[str, Path],
        include_comments: bool = True,
    ) -> Path:
        path = Path(output_path)
        text = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        path = Path(hex_file_path)
        if not path.is_file():
            return False

        token_re = re.compile(r"^(?:0x)?[0-9A-Fa-f]{8}$")
        found_any = False

        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            body = line.split("#", 1)[0].strip()
            if not body:
                continue
            tokens = body.split()
            for tok in tokens:
                if not token_re.fullmatch(tok):
                    return False
            found_any = True

        return found_any

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        if not isinstance(config_space_data, (bytes, bytearray)):
            raise TypeError("config_space_data must be bytes-like")
        data = bytes(config_space_data)
        if len(data) == 0:
            return []
        if len(data) % 4 != 0:
            pad_len = 4 - (len(data) % 4)
            data += b"\x00" * pad_len
        dwords: List[int] = []
        for i in range(0, len(data), 4):
            chunk = data[i: i + 4]
            val = int.from_bytes(chunk, byteorder="little", signed=False)
            dwords.append(val)
        return dwords
