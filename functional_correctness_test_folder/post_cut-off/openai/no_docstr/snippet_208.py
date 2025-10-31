
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple


class OptionROMManager:
    """
    A helper class to extract, load, and inspect PCI option ROMs on Linux.
    """

    def __init__(self, output_dir: Optional[Path] = None, rom_file_path: Optional[str] = None):
        """
        Parameters
        ----------
        output_dir : Optional[Path]
            Directory where extracted ROMs will be stored. Defaults to the current working directory.
        rom_file_path : Optional[str]
            Path to an existing ROM file to load. If None, no ROM is loaded initially.
        """
        self.output_dir: Path = Path(output_dir) if output_dir else Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rom_file_path: Optional[Path] = Path(
            rom_file_path) if rom_file_path else None
        self.rom_data: Optional[bytes] = None

        if self.rom_file_path and self.rom_file_path.is_file():
            self.load_rom_file(str(self.rom_file_path))

    # ------------------------------------------------------------------
    # Extraction helpers
    # ------------------------------------------------------------------
    def _parse_lspci_output(self, output: str) -> Optional[str]:
        """
        Parse the output of `lspci -vvv -s <bdf>` to find the ROM file path.
        """
        # lspci may show something like: "ROM at /sys/bus/pci/devices/0000:00:1f.2/rom"
        match = re.search(r"ROM at\s+(\S+)", output)
        if match:
            return match.group(1)
        return None

    def extract_rom_linux(self, bdf: str) -> Tuple[bool, str]:
        """
        Extract the option ROM for the device identified by the PCI BDF string.

        Parameters
        ----------
        bdf : str
            PCI bus/device/function identifier (e.g., "0000:00:1f.2").

        Returns
        -------
        Tuple[bool, str]
            (True, path_to_extracted_rom) on success,
            (False, error_message) on failure.
        """
        try:
            cmd = ["lspci", "-vvv", "-s", bdf]
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True)
            rom_path = self._parse_lspci_output(result.stdout)
            if not rom_path:
                return False, f"ROM not found for device {bdf}"
            rom_source = Path(rom_path)
            if not rom_source.is_file():
                return False, f"ROM file does not exist: {rom_source}"
            dest_path = self.output_dir / f"{bdf.replace(':', '_')}_rom.bin"
            shutil.copyfile(rom_source, dest_path)
            self.rom_file_path = dest_path
            self.load_rom_file(str(dest_path))
            return True, str(dest_path)
        except subprocess.CalledProcessError as e:
            return False, f"lspci command failed: {e}"
        except Exception as exc:
            return False, f"Unexpected error: {exc}"

    # ------------------------------------------------------------------
    # ROM file handling
    # ------------------------------------------------------------------
    def load_rom_file(self, file_path: Optional[str] = None) -> bool:
        """
        Load a ROM file into memory.

        Parameters
        ----------
        file_path : Optional[str]
            Path to the ROM file. If None, uses the previously set rom_file_path.

        Returns
        -------
        bool
            True if the file was loaded successfully, False otherwise.
        """
        path = Path(file_path) if file_path else self.rom_file_path
        if not path or not path.is_file():
            return False
        try:
            with path.open("rb") as f:
                self.rom_data = f.read()
            self.rom_file_path = path
            return True
        except Exception:
            return False

    def save_rom_hex(self, output_path: Optional[str] = None) -> bool:
        """
        Save the loaded ROM data as a hex dump.

        Parameters
        ----------
        output_path : Optional[str]
            Destination file path. If None, uses the rom_file_path with a .hex suffix.

        Returns
        -------
        bool
            True on success, False otherwise.
        """
        if not self.rom_data:
            return False
        out_path = Path(output_path) if output_path else (
            self.rom_file_path.with_suffix(".hex") if self.rom_file_path else None)
        if not out_path:
            return False
        try:
            hex_str = self.rom_data.hex()
            with out_path.open("w") as f:
                f.write(hex_str)
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Information extraction
    # ------------------------------------------------------------------
    def get_rom_info(self) -> Dict[str, str]:
        """
        Return basic information about the loaded ROM.

        Returns
        -------
        Dict[str, str]
            Dictionary containing size, SHA-256 checksum, and first 8 bytes in hex.
        """
        if not self.rom_data:
            return {}
        size = len(self.rom_data)
        sha256 = hashlib.sha256(self.rom_data).hexdigest()
        first_bytes = self.rom_data[:8].hex()
        return {
            "size_bytes": str(size),
            "sha256": sha256,
            "first_8_bytes": first_bytes,
            "rom_path": str(self.rom_file_path) if self.rom_file_path else "",
        }

    # ------------------------------------------------------------------
    # High‑level orchestration
    # ------------------------------------------------------------------
    def setup_option_rom(self, bdf: str, use_existing_rom: bool = False) -> Dict[str, str]:
        """
        Ensure that a ROM is available for the given device.

        Parameters
        ----------
        bdf : str
            PCI bus/device/function identifier.
        use_existing_rom : bool
            If True and a rom_file_path is already set, skip extraction.

        Returns
        -------
        Dict[str, str]
            Information about the ROM (size, checksum, etc.).
        """
        if use_existing_rom and self.rom_file_path and self.rom_file_path.is_file():
            if not self.load_rom_file():
                # If loading fails, fall back to extraction
                pass
            else:
                return self.get_rom_info()

        # Otherwise, attempt extraction
        success, msg = self.extract_rom_linux(bdf)
        if not success:
            raise RuntimeError(f"Failed to set up ROM for {bdf}: {msg}")

        return self.get_rom_info()
