
import re
from typing import List, Dict, Any, Union


class Transcript:
    '''
    Container for transcript methods.
    '''
    @staticmethod
    def _parse_time(time_str: str) -> float:
        """Convert 'HH:MM:SS,ms' to seconds."""
        h, m, s_ms = time_str.split(':')
        s, ms = s_ms.split(',')
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Convert seconds to 'HH:MM:SS,ms'."""
        ms = int(round((seconds - int(seconds)) * 1000))
        total_seconds = int(seconds)
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    @staticmethod
    def generate_sjson_from_srt(srt_subs: str) -> Dict[str, Any]:
        """
        Generate transcripts from sjson to SubRip (*.srt).
        Arguments:
            srt_subs (str): SRT subtitle content.
        Returns:
            dict: Subtitles converted to "SJSON" format.
        """
        if not isinstance(srt_subs, str):
            raise TypeError("srt_subs must be a string containing SRT data")

        entries: List[Dict[str, Any]] = []
        blocks = re.split(r'\n\s*\n', srt_subs.strip(), flags=re.MULTILINE)
        for block in blocks:
            lines = block.strip().splitlines()
            if len(lines) < 2:
                continue
            # first line is index (ignored)
            time_line = lines[1]
            match = re.match(
                r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})', time_line)
            if not match:
                continue
            start_str, end_str = match.groups()
            start = Transcript._parse_time(start_str)
            end = Transcript._parse_time(end_str)
            text = "\n".join(lines[2:]).strip()
            entries.append({
                "start": start,
                "end": end,
                "text": text
            })
        return {"subtitles": entries}

    @staticmethod
    def generate_srt_from_sjson(sjson_subs: Dict[str, Any]) -> str:
        """
        Generate transcripts from sjson to SubRip (*.srt)
        Arguments:
            sjson_subs (dict): `sjson` subs.
        Returns:
            str: Subtitles in SRT format.
        """
        if not isinstance(sjson_subs, dict):
            raise TypeError("sjson_subs must be a dictionary")
        subtitles = sjson_subs.get("subtitles")
        if subtitles is None:
            raise ValueError("sjson_subs must contain 'subtitles' key")
        srt_blocks = []
        for idx, entry in enumerate(subtitles, start=1):
            start = entry.get("start")
            end = entry.get("end")
            text = entry.get("text", "")
            if start is None or end is None:
                continue
            start_str = Transcript._format_time(float(start))
            end_str = Transcript._format_time(float(end))
            block = f"{idx}\n{start_str} --> {end_str}\n{text}"
            srt_blocks.append(block)
        return "\n\n".join(srt_blocks)

    @classmethod
    def convert(cls, content: Union[str, Dict[str, Any]], input_format: str, output_format: str) -> Union[str, Dict[str, Any]]:
        """
        Convert subtitle content between formats.
        Arguments:
            content: Subtitle data (string for SRT, dict for SJSON).
            input_format: 'srt' or 'sjson'.
            output_format: 'srt' or 'sjson'.
        Returns:
            Converted subtitle data.
        """
        input_format = input_format.lower()
        output_format = output_format.lower()
        if input_format == output_format:
            return content

        if input_format == "srt" and output_format == "sjson":
            return cls.generate_sjson_from_srt(content)
        if input_format == "sjson" and output_format == "srt":
            return cls.generate_srt_from_sjson(content)

        raise ValueError(
            f"Unsupported conversion from {input_format} to {output_format}")
