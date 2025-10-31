
import re
import json
from typing import List, Dict, Any, Union


class TranscriptsGenerationException(Exception):
    """Raised when a transcript cannot be parsed or generated."""
    pass


class Transcript:
    """
    Container for transcript methods.
    """

    _TIME_RE = re.compile(
        r"(?P<h>\d{2}):(?P<m>\d{2}):(?P<s>\d{2}),(?P<ms>\d{3})"
    )

    @staticmethod
    def _time_str_to_seconds(time_str: str) -> float:
        """Convert HH:MM:SS,ms to seconds."""
        m = Transcript._TIME_RE.match(time_str)
        if not m:
            raise TranscriptsGenerationException(
                f"Invalid time format: {time_str}")
        h = int(m.group("h"))
        m_ = int(m.group("m"))
        s = int(m.group("s"))
        ms = int(m.group("ms"))
        return h * 3600 + m_ * 60 + s + ms / 1000.0

    @staticmethod
    def _seconds_to_time_str(seconds: float) -> str:
        """Convert seconds to HH:MM:SS,ms."""
        ms = int(round((seconds - int(seconds)) * 1000))
        s = int(seconds) % 60
        m = (int(seconds) // 60) % 60
        h = int(seconds) // 3600
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    @staticmethod
    def generate_sjson_from_srt(srt_subs: Union[str, bytes]) -> Dict[str, Any]:
        """
        Generate transcripts from sjson to SubRip (*.srt).
        Arguments:
            srt_subs(SubRip): "SRT" subs object
        Returns:
            Subs converted to "SJSON" format.
        """
        if isinstance(srt_subs, bytes):
            srt_subs = srt_subs.decode("utf-8")

        lines = srt_subs.splitlines()
        subtitles: List[Dict[str, Any]] = []
        i = 0
        while i < len(lines):
            # Skip empty lines
            if not lines[i].strip():
                i += 1
                continue

            # Index line
            try:
                idx = int(lines[i].strip())
            except ValueError:
                raise TranscriptsGenerationException(
                    f"Expected subtitle index at line {i+1}"
                )
            i += 1

            # Time range line
            if i >= len(lines):
                raise TranscriptsGenerationException(
                    "Unexpected end of file after index")
            time_line = lines[i].strip()
            i += 1
            if " --> " not in time_line:
                raise TranscriptsGenerationException(
                    f"Invalid time range at line {i}")
            start_str, end_str = [t.strip() for t in time_line.split(" --> ")]
            start = Transcript._time_str_to_seconds(start_str)
            end = Transcript._time_str_to_seconds(end_str)

            # Text lines
            text_lines = []
            while i < len(lines) and lines[i].strip():
                text_lines.append(lines[i])
                i += 1
            text = "\n".join(text_lines)

            subtitles.append(
                {"index": idx, "start": start, "end": end, "text": text}
            )

        return {"subtitles": subtitles}

    @staticmethod
    def generate_srt_from_sjson(sjson_subs: Dict[str, Any]) -> str:
        """
        Generate transcripts from sjson to SubRip (*.srt)
        Arguments:
            sjson_subs (dict): `sjson` subs.
        Returns:
            Subtitles in SRT format.
        """
        if "subtitles" not in sjson_subs:
            raise TranscriptsGenerationException(
                "Missing 'subtitles' key in sjson")

        srt_lines: List[str] = []
        for idx, entry in enumerate(sjson_subs["subtitles"], start=1):
            start = entry.get("start")
            end = entry.get("end")
            text = entry.get("text", "")
            if start is None or end is None:
                raise TranscriptsGenerationException(
                    f"Subtitle {idx} missing start or end time"
                )
            start_str = Transcript._seconds_to_time_str(float(start))
            end_str = Transcript._seconds_to_time_str(float(end))
            srt_lines.append(str(idx))
            srt_lines.append(f"{start_str} --> {end_str}")
            srt_lines.append(text)
            srt_lines.append("")  # blank line

        return "\n".join(srt_lines)

    @classmethod
    def convert(
        cls,
        content: bytes,
        input_format: str,
        output_format: str,
    ) -> Union[str, Dict[str, Any]]:
        """
        Convert transcript `content` from `input_format` to `output_format`.
        Arguments:
            content: Transcript content byte-stream.
            input_format: Input transcript format.
            output_format: Output transcript format.
        Accepted input formats: sjson, srt.
        Accepted output format: srt, sjson.
        Raises:
            TranscriptsGenerationException: On parsing the invalid srt
            content during conversion from srt to sjson.
        """
        if not isinstance(content, bytes):
            raise TypeError("content must be bytes")

        input_format = input_format.lower()
        output_format = output_format.lower()

        if input_format == output_format:
            # Return decoded string
            return content.decode("utf-8")

        if input_format == "srt" and output_format == "sjson":
            srt_text = content.decode("utf-8")
            return cls.generate_sjson_from_srt(srt_text)

        if input_format == "sjson" and output_format == "srt":
            try:
                sjson_obj = json.loads(content.decode("utf-8"))
            except json.JSONDecodeError as e:
                raise TranscriptsGenerationException("Invalid JSON") from e
            return cls.generate_srt_from_sjson(sjson_obj)

        raise TranscriptsGenerationException(
            f"Unsupported conversion: {input_format} -> {output_format}"
        )
