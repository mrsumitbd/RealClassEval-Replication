
from typing import Optional, Union, List
from pathlib import Path


class ConfigSpaceHexFormatter:

    def __init__(self):
        # Initialize an empty dictionary to store register comments
        self.register_comments = {
            0x00: "Vendor ID",
            0x02: "Device ID",
            0x04: "Command",
            0x06: "Status",
            0x08: "Revision ID",
            0x09: "Class Code",
            0x0C: "Cache Line Size",
            0x0D: "Latency Timer",
            0x0E: "Header Type",
            0x0F: "BIST",
            # Add more register comments as needed
        }

    def format_config_space_to_hex(self, config_space_data: bytes, include_comments: bool = True, words_per_line: int = 1, vendor_id: Optional[str] = None, device_id: Optional[str] = None, class_code: Optional[str] = None, board: Optional[str] = None) -> str:
        # Convert config space data to a list of DWORDs
        dword_list = self.convert_to_dword_list(config_space_data)

        # Initialize the output string
        output = ""

        # Add a header if any of the optional parameters are provided
        if vendor_id or device_id or class_code or board:
            output += f"# Vendor ID: {vendor_id or 'Unknown'}\n"
            output += f"# Device ID: {device_id or 'Unknown'}\n"
            output += f"# Class Code: {class_code or 'Unknown'}\n"
            output += f"# Board: {board or 'Unknown'}\n\n"

        # Iterate over the DWORDs and format them as hex
        for i, dword in enumerate(dword_list):
            offset = i * 4
            comment = self._get_register_comment(
                offset) if include_comments else None
            output += f"{dword:08X}"  # Format as 8-digit hex

            # Add a comment if available
            if comment:
                output += f"  # {comment}"

            # Add a newline if this is the last word on the line
            if (i + 1) % words_per_line == 0:
                output += "\n"
            else:
                output += " "

        return output.strip()  # Remove trailing whitespace

    def _get_register_comment(self, offset: int) -> Optional[str]:
        # Return a comment for the register at the given offset
        return self.register_comments.get(offset)

    def write_hex_file(self, config_space_data: bytes, output_path: Union[str, Path], include_comments: bool = True) -> Path:
        # Convert the output path to a Path object
        output_path = Path(output_path)

        # Format the config space data as hex
        hex_data = self.format_config_space_to_hex(
            config_space_data, include_comments=include_comments)

        # Write the hex data to the output file
        with output_path.open("w") as f:
            f.write(hex_data)

        return output_path

    def validate_hex_file(self, hex_file_path: Union[str, Path]) -> bool:
        # Convert the hex file path to a Path object
        hex_file_path = Path(hex_file_path)

        # Check if the file exists
        if not hex_file_path.exists():
            return False

        # Try to read the file and validate its contents
        try:
            with hex_file_path.open("r") as f:
                for line in f:
                    # Remove comments and whitespace
                    line = line.split("#")[0].strip()

                    # Check if the line is empty
                    if not line:
                        continue

                    # Try to parse the line as hex
                    try:
                        int(line, 16)
                    except ValueError:
                        return False
        except Exception:
            return False

        return True

    def convert_to_dword_list(self, config_space_data: bytes) -> List[int]:
        # Convert the config space data to a list of DWORDs
        dword_list = []
        for i in range(0, len(config_space_data), 4):
            dword = int.from_bytes(config_space_data[i:i+4], "little")
            dword_list.append(dword)
        return dword_list
