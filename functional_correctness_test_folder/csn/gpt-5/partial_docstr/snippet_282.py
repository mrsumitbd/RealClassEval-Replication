class Transcript:
    '''
    Container for transcript methods.
    '''
    @staticmethod
    def _parse_timecode_to_ms(tc):
        if not isinstance(tc, str):
            raise ValueError("Timecode must be a string")
        t = tc.strip().replace(',', '.')
        parts = t.split(':')
        if len(parts) != 3:
            raise ValueError(f"Invalid timecode: {tc}")
        h = int(parts[0])
        m = int(parts[1])
        s_parts = parts[2].split('.')
        s = int(s_parts[0])
        ms = int((s_parts[1] + '000')[:3]) if len(s_parts) > 1 else 0
        return ((h * 60 + m) * 60 + s) * 1000 + ms

    @staticmethod
    def _format_ms_to_timecode(ms):
        if ms < 0:
            ms = 0
        total_ms = int(round(ms))
        h = total_ms // 3600000
        rem = total_ms % 3600000
        m = rem // 60000
        rem = rem % 60000
        s = rem // 1000
        msec = rem % 1000
        return f"{h:02d}:{m:02d}:{s:02d},{msec:03d}"

    @staticmethod
    def _to_int_ms(value):
        # Accept ms (int), seconds (float), or strings convertible to either.
        if isinstance(value, (int,)):
            return int(value)
        if isinstance(value, float):
            return int(round(value * 1000))
        if isinstance(value, str):
            v = value.strip()
            # Try SRT-like timecode
            if ':' in v:
                return Transcript._parse_timecode_to_ms(v)
            # Try numeric
            try:
                if '.' in v:
                    return int(round(float(v) * 1000))
                return int(v)
            except ValueError:
                pass
        raise ValueError(f"Unsupported time value: {value}")

    @staticmethod
    def _split_srt_blocks(s):
        import re
        # Normalize newlines and split on blank lines (handles one or more blank lines)
        s = s.replace('\r\n', '\n').replace('\r', '\n')
        # Remove BOM if present
        if s.startswith('\ufeff'):
            s = s.lstrip('\ufeff')
        blocks = re.split(r'\n{2,}', s.strip())
        return [b for b in blocks if b.strip()]

    @staticmethod
    def generate_sjson_from_srt(srt_subs):
        '''
        Generate transcripts from sjson to SubRip (*.srt).
        Arguments:
            srt_subs(SubRip): "SRT" subs object
        Returns:
            Subs converted to "SJSON" format.
        '''
        # Accept string content of SRT
        if not isinstance(srt_subs, str):
            raise TypeError("srt_subs must be a string containing SRT data")

        blocks = Transcript._split_srt_blocks(srt_subs)
        fragments = []
        idx_counter = 1
        for block in blocks:
            lines = [ln for ln in block.split('\n')]
            if not lines:
                continue
            # Detect if first line is index
            time_line_idx = 0
            index_val = None
            if lines and lines[0].strip().isdigit():
                index_val = int(lines[0].strip())
                time_line_idx = 1
            # Find time line containing -->
            if time_line_idx >= len(lines) or '-->' not in lines[time_line_idx]:
                # Try to locate a line with -->
                found = None
                for i, ln in enumerate(lines):
                    if '-->' in ln:
                        found = i
                        break
                if found is None:
                    # Skip malformed block
                    continue
                time_line_idx = found
            time_line = lines[time_line_idx]
            parts = time_line.split('-->')
            if len(parts) != 2:
                continue
            start_tc = parts[0].strip()
            end_tc = parts[1].strip()
            try:
                start_ms = Transcript._parse_timecode_to_ms(start_tc)
                end_ms = Transcript._parse_timecode_to_ms(end_tc)
            except Exception:
                continue

            text_lines = lines[time_line_idx +
                               1:] if time_line_idx + 1 < len(lines) else []
            # Trim trailing empty lines
            while text_lines and text_lines[-1].strip() == '':
                text_lines.pop()
            text = '\n'.join(text_lines).strip()
            fragments.append({
                "id": index_val if index_val is not None else idx_counter,
                "start": start_ms,
                "end": end_ms,
                "text": text
            })
            idx_counter += 1

        return {
            "type": "transcript",
            "format": "sjson",
            "fragments": fragments
        }

    @staticmethod
    def generate_srt_from_sjson(sjson_subs):
        '''
        Generate transcripts from sjson to SubRip (*.srt)
        Arguments:
            sjson_subs (dict): `sjson` subs.
        Returns:
            Subtitles in SRT format.
        '''
        import json

        data = sjson_subs
        if isinstance(sjson_subs, str):
            data = json.loads(sjson_subs)
        if not isinstance(data, dict):
            raise TypeError("sjson_subs must be a dict or a JSON string")
        fragments = data.get("fragments") or data.get(
            "segments") or data.get("items")
        if not isinstance(fragments, list):
            raise ValueError("Invalid sjson structure: missing fragments list")

        def frag_start_ms(f):
            if "start" in f:
                return Transcript._to_int_ms(f["start"])
            if "begin" in f:
                return Transcript._to_int_ms(f["begin"])
            if "ts" in f:
                return Transcript._to_int_ms(f["ts"])
            return 0

        srt_lines = []
        # Sort by start time if not already
        fragments_sorted = sorted(fragments, key=frag_start_ms)

        for i, f in enumerate(fragments_sorted, start=1):
            # Determine start and end
            if "start" in f:
                start_ms = Transcript._to_int_ms(f["start"])
            elif "begin" in f:
                start_ms = Transcript._to_int_ms(f["begin"])
            elif "ts" in f:
                start_ms = Transcript._to_int_ms(f["ts"])
            else:
                start_ms = 0

            if "end" in f:
                end_ms = Transcript._to_int_ms(f["end"])
            elif "duration" in f:
                end_ms = start_ms + Transcript._to_int_ms(f["duration"])
            elif "dur" in f:
                end_ms = start_ms + Transcript._to_int_ms(f["dur"])
            else:
                # Fallback: add 2 seconds
                end_ms = start_ms + 2000

            # Determine text
            if "text" in f and isinstance(f["text"], str):
                text = f["text"]
            elif "lines" in f and isinstance(f["lines"], list):
                text = "\n".join(str(x) for x in f["lines"])
            elif "content" in f:
                text = str(f["content"])
            else:
                text = ""

            start_tc = Transcript._format_ms_to_timecode(start_ms)
            end_tc = Transcript._format_ms_to_timecode(end_ms)
            srt_lines.append(str(i))
            srt_lines.append(f"{start_tc} --> {end_tc}")
            # Ensure no CRLF inside text
            if text:
                text_norm = text.replace('\r\n', '\n').replace('\r', '\n')
                srt_lines.extend(text_norm.split('\n'))
            srt_lines.append("")  # blank line after each block

        return "\n".join(srt_lines).rstrip() + "\n"

    @classmethod
    def convert(cls, content, input_format, output_format):
        input_fmt = (input_format or "").strip().lower()
        output_fmt = (output_format or "").strip().lower()

        if input_fmt == output_fmt:
            return content

        if input_fmt == "srt" and output_fmt == "sjson":
            if not isinstance(content, str):
                raise TypeError("For srt input, content must be a string")
            return cls.generate_sjson_from_srt(content)

        if input_fmt == "sjson" and output_fmt == "srt":
            return cls.generate_srt_from_sjson(content)

        raise ValueError(
            f"Unsupported conversion: {input_format} -> {output_format}")
