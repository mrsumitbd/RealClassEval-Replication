from pathlib import Path
from typing import Optional, Tuple, Dict
import os
import sys
import binascii


class OptionROMManager:
    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        self.output_dir: Path = Path(
            output_dir) if output_dir else Path.cwd() / "option_rom_output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rom_file_path: Optional[str] = rom_file_path
        self.rom_bytes: Optional[bytes] = None
        self.extracted_file_path: Optional[Path] = None
        self.hex_file_path: Optional[Path] = None

    def _normalize_bdf(self, bdf: str) -> str:
        bdf = bdf.strip()
        if bdf.count(":") == 1:
            return f"0000:{bdf}"
        return bdf

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        if sys.platform != "linux":
            return False, "Option ROM extraction is only supported on Linux."
        try:
            bdf_norm = self._normalize_bdf(bdf)
            dev_dir = Path("/sys/bus/pci/devices") / bdf_norm
            rom_path = dev_dir / "rom"
            if not dev_dir.exists():
                return False, f"PCI device not found: {bdf_norm}"
            if not rom_path.exists():
                return False, f"ROM sysfs node not found: {rom_path}"

            try:
                with open(rom_path, "wb", buffering=0) as f:
                    f.write(b"1")
            except PermissionError:
                return False, f"Permission denied enabling ROM read: {rom_path}. Try as root."

            data = b""
            err = None
            try:
                with open(rom_path, "rb", buffering=0) as f:
                    data = f.read()
            except Exception as e:
                err = str(e)
            finally:
                try:
                    with open(rom_path, "wb", buffering=0) as f:
                        f.write(b"0")
                except Exception:
                    pass

            if err:
                return False, f"Failed reading ROM: {err}"
            if not data:
                return False, "ROM appears empty."

            self.rom_bytes = data
            out_bin = self.output_dir / \
                f"{bdf_norm.replace(':', '_').replace('.', '_')}_option_rom.bin"
            with open(out_bin, "wb") as f:
                f.write(data)
            self.extracted_file_path = out_bin
            self.rom_file_path = str(out_bin)
            return True, f"ROM extracted to {out_bin}"
        except Exception as e:
            return False, f"Unexpected error: {e}"

    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        path = file_path or self.rom_file_path
        if not path:
            return False
        p = Path(path)
        if not p.exists() or not p.is_file():
            return False
        try:
            self.rom_bytes = p.read_bytes()
            self.rom_file_path = str(p)
            return True
        except Exception:
            return False

    def save_rom_hex(self, output_path: Optional[str] = None) -> bool:
        if not self.rom_bytes:
            return False
        try:
            out_path = Path(output_path) if output_path else (
                self.output_dir / "option_rom.hex")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            hexstr = binascii.hexlify(self.rom_bytes).decode("ascii")
            # Write 16 bytes per line (32 hex chars), spaced for readability
            with open(out_path, "w", encoding="utf-8") as f:
                for i in range(0, len(hexstr), 32):
                    line = hexstr[i: i + 32]
                    spaced = " ".join(line[j: j + 2]
                                      for j in range(0, len(line), 2))
                    f.write(spaced + "\n")
            self.hex_file_path = out_path
            return True
        except Exception:
            return False

    def get_rom_info(self) -> Dict[str, str]:
        info: Dict[str, str] = {}
        data = self.rom_bytes or b""
        size = len(data)
        info["size_bytes"] = str(size)
        sig_ok = size >= 2 and data[0] == 0x55 and data[1] == 0xAA
        info["signature_valid"] = "true" if sig_ok else "false"

        total_len_reported = ""
        if size >= 3:
            units = data[2]
            total_len = units * 512
            if total_len > 0:
                total_len_reported = str(total_len)
        info["reported_total_length"] = total_len_reported

        pcir_present = "false"
        vendor_id = ""
        device_id = ""
        try:
            if size >= 0x1A:
                pcir_ptr = int.from_bytes(data[0x18:0x1A], "little")
                if 0 <= pcir_ptr <= size - 4 and data[pcir_ptr: pcir_ptr + 4] == b"PCIR":
                    pcir_present = "true"
                    if pcir_ptr + 8 <= size:
                        vendor_id = f"0x{int.from_bytes(data[pcir_ptr+4:pcir_ptr+6], 'little'):04X}"
                        device_id = f"0x{int.from_bytes(data[pcir_ptr+6:pcir_ptr+8], 'little'):04X}"
        except Exception:
            pass

        info["pcir_present"] = pcir_present
        if vendor_id:
            info["vendor_id"] = vendor_id
        if device_id:
            info["device_id"] = device_id

        info["rom_file"] = self.rom_file_path or ""
        info["hex_file"] = str(
            self.hex_file_path) if self.hex_file_path else ""
        info["source"] = (
            "extracted" if self.extracted_file_path and self.rom_file_path == str(
                self.extracted_file_path) else "file"
            if self.rom_file_path
            else ""
        )
        return info

    def setup_option_rom(self, bdf: str, use_existing_rom: bool = False) -> Dict[str, str]:
        result: Dict[str, str] = {}
        success = False
        message = ""

        if use_existing_rom:
            if not self.rom_file_path:
                result["status"] = "error"
                result["message"] = "No ROM file path specified."
                return result
            success = self.load_rom_file(self.rom_file_path)
            message = "Loaded ROM from file." if success else "Failed to load ROM file."
        else:
            success, message = self.extract_rom_linux(bdf)

        result["status"] = "ok" if success else "error"
        result["message"] = message

        if success:
            self.save_rom_hex()
            result.update(self.get_rom_info())

        return result
