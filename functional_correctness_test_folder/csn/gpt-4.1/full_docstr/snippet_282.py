
class TranscriptsGenerationException(Exception):
    pass


class Transcript:
    '''
    Container for transcript methods.
    '''
    @staticmethod
    def generate_sjson_from_srt(srt_subs):
        '''
        Generate transcripts from sjson to SubRip (*.srt).
        Arguments:
            srt_subs(SubRip): "SRT" subs object
        Returns:
            Subs converted to "SJSON" format.
        '''
        sjson = {"transcript": []}
        for sub in srt_subs:
            sjson["transcript"].append({
                "start": sub["start"],
                "end": sub["end"],
                "text": sub["text"]
            })
        return sjson

    @staticmethod
    def generate_srt_from_sjson(sjson_subs):
        '''
        Generate transcripts from sjson to SubRip (*.srt)
        Arguments:
            sjson_subs (dict): `sjson` subs.
        Returns:
            Subtitles in SRT format.
        '''
        def format_time(seconds):
            import math
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            ms = int(round((seconds - int(seconds)) * 1000))
            return f"{h:02}:{m:02}:{s:02},{ms:03}"

        srt_lines = []
        for idx, entry in enumerate(sjson_subs.get("transcript", []), 1):
            start = format_time(entry["start"])
            end = format_time(entry["end"])
            text = entry["text"]
            srt_lines.append(f"{idx}\n{start} --> {end}\n{text}\n")
        return "\n".join(srt_lines).strip()

    @classmethod
    def convert(cls, content, input_format, output_format):
        '''
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
        '''
        import json

        def parse_srt(srt_str):
            import re
            pattern = re.compile(
                r'(\d+)\s*\n(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*\n(.*?)(?=\n{2,}|\Z)',
                re.DOTALL
            )

            def parse_time(t):
                h, m, s_ms = t.split(":")
                s, ms = s_ms.split(",")
                return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

            subs = []
            for match in pattern.finditer(srt_str):
                idx, start, end, text = match.groups()
                try:
                    start_sec = parse_time(start)
                    end_sec = parse_time(end)
                except Exception:
                    raise TranscriptsGenerationException(
                        "Invalid SRT time format")
                subs.append({
                    "index": int(idx),
                    "start": start_sec,
                    "end": end_sec,
                    "text": text.strip().replace('\r\n', '\n').replace('\r', '\n')
                })
            if not subs and srt_str.strip():
                raise TranscriptsGenerationException("Invalid SRT format")
            return subs

        def srt_obj_to_sjson(srt_obj):
            return cls.generate_sjson_from_srt(srt_obj)

        def sjson_to_srt(sjson_obj):
            return cls.generate_srt_from_sjson(sjson_obj)

        if input_format == "sjson":
            try:
                if isinstance(content, (bytes, bytearray)):
                    sjson_obj = json.loads(content.decode("utf-8"))
                elif isinstance(content, str):
                    sjson_obj = json.loads(content)
                else:
                    sjson_obj = content
            except Exception:
                raise TranscriptsGenerationException("Invalid SJSON format")
            if output_format == "sjson":
                return json.dumps(sjson_obj, ensure_ascii=False, indent=2)
            elif output_format == "srt":
                return sjson_to_srt(sjson_obj)
            else:
                raise ValueError("Unsupported output format")
        elif input_format == "srt":
            if isinstance(content, (bytes, bytearray)):
                srt_str = content.decode("utf-8")
            elif isinstance(content, str):
                srt_str = content
            else:
                raise TranscriptsGenerationException(
                    "Invalid SRT content type")
            try:
                srt_obj = parse_srt(srt_str)
            except TranscriptsGenerationException as e:
                raise
            if output_format == "sjson":
                sjson_obj = srt_obj_to_sjson(srt_obj)
                return json.dumps(sjson_obj, ensure_ascii=False, indent=2)
            elif output_format == "srt":
                # Reformat SRT (normalize)
                sjson_obj = srt_obj_to_sjson(srt_obj)
                return sjson_to_srt(sjson_obj)
            else:
                raise ValueError("Unsupported output format")
        else:
            raise ValueError("Unsupported input format")
