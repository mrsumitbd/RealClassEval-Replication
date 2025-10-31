
import json
import re
from typing import List, Dict, Any


class Transcript:
    @staticmethod
    def generate_sjson_from_srt(srt_subs: str) -> str:
        """
        Convert SRT subtitle string to SJSON (JSON list of subtitle objects).
        Each subtitle object contains:
            - start: start time string "HH:MM:SS,mmm"
            - end:   end time string "HH:MM:SS,mmm"
            - text:  subtitle text (single string with newlines preserved)
        """
        # Normalize line endings
        srt_subs = srt_subs.replace('\r\n', '\n').replace('\r', '\n')
        # Split into blocks separated by blank lines
        blocks = [b.strip() for b in srt_subs.split('\n\n') if b.strip()]
        subs: List[Dict[str, Any]] = []

        time_pattern = re.compile(
            r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})')

        for block in blocks:
            lines = block.split('\n')
            if len(lines) < 3:
                continue  # Not a valid subtitle block
            # First line is index (ignored)
            # Second line is time
            time_match = time_pattern.match(lines[1].strip())
            if not time_match:
                continue  # Invalid time format
            start, end = time_match.groups()
            # Remaining lines are text
            text = '\n'.join(lines[2:])
            subs.append({'start': start, 'end': end, 'text': text})

        return json.dumps(subs, ensure_ascii=False, indent=2)

    @staticmethod
    def generate_srt_from_sjson(sjson_subs: List[Dict[str, Any]]) -> str:
        """
        Convert SJSON (list of subtitle objects) to SRT subtitle string.
        Each subtitle object must contain 'start', 'end', and 'text'.
        """
        srt_blocks = []
        for idx, sub in enumerate(sjson_subs, start=1):
            start = sub.get('start')
            end = sub.get('end')
            text = sub.get('text', '')
            if not start or not end:
                continue  # Skip invalid entries
            block = f"{idx}\n{start} --> {end}\n{text}"
            srt_blocks.append(block)
        return '\n\n'.join(srt_blocks) + '\n'

    @classmethod
    def convert(cls, content: str, input_format: str, output_format: str) -> str:
        """
        Convert subtitle content between SRT and SJSON formats.
        Supported formats: 'srt', 'sjson'.
        """
        input_format = input_format.lower()
        output_format = output_format.lower()

        if input_format == output_format:
            return content  # No conversion needed

        if input_format == 'srt':
            # Parse SRT to SJSON
            sjson = json.loads(cls.generate_sjson_from_srt(content))
            if output_format == 'sjson':
                return json.dumps(sjson, ensure_ascii=False, indent=2)
            elif output_format == 'srt':
                return cls.generate_srt_from_sjson(sjson)
            else:
                raise ValueError(f"Unsupported output format: {output_format}")

        elif input_format == 'sjson':
            # Parse SJSON to Python list
            try:
                subs = json.loads(content)
            except json.JSONDecodeError as e:
                raise ValueError("Invalid JSON content") from e
            if output_format == 'srt':
                return cls.generate_srt_from_sjson(subs)
            elif output_format == 'sjson':
                return json.dumps(subs, ensure_ascii=False, indent=2)
            else:
                raise ValueError(f"Unsupported output format: {output_format}")

        else:
            raise ValueError(f"Unsupported input format: {input_format}")
