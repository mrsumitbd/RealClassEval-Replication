class Transcript:

    @staticmethod
    def _parse_srt_timestamp(ts):
        ts = ts.strip()
        # Accept "HH:MM:SS,mmm" or "HH:MM:SS.mmm"
        hms, ms = ts.replace(',', '.').split('.')
        h, m, s = hms.split(':')
        total = int(h) * 3600 + int(m) * 60 + int(s) + \
            int(ms.ljust(3, '0')[:3]) / 1000.0
        return total

    @staticmethod
    def _format_srt_timestamp(seconds):
        if seconds < 0:
            seconds = 0
        total_ms = int(round(seconds * 1000))
        h = total_ms // 3600000
        rem = total_ms % 3600000
        m = rem // 60000
        rem = rem % 60000
        s = rem // 1000
        ms = rem % 1000
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    @staticmethod
    def generate_sjson_from_srt(srt_subs):
        import json
        if not isinstance(srt_subs, str):
            raise TypeError("srt_subs must be a string")
        text = srt_subs.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
        if not text:
            return json.dumps({"segments": []}, ensure_ascii=False)
        blocks = []
        current = []
        for line in text.split("\n"):
            if line.strip() == "":
                if current:
                    blocks.append(current)
                    current = []
            else:
                current.append(line)
        if current:
            blocks.append(current)

        segments = []
        seq = 1
        for blk in blocks:
            # Expected:
            # [index?], timing line, text lines...
            # Identify timing line containing -->
            idx = None
            timing_line_idx = None
            # timing line usually in first two lines
            for i, line in enumerate(blk[:2]):
                if "-->" in line:
                    timing_line_idx = i
                    break
            if timing_line_idx is None:
                # Fallback: search anywhere
                for i, line in enumerate(blk):
                    if "-->" in line:
                        timing_line_idx = i
                        break
            if timing_line_idx is None:
                # Cannot parse timing; skip block
                continue
            # Try index from previous line if numeric
            if timing_line_idx >= 1:
                try:
                    maybe_idx = blk[timing_line_idx - 1].strip()
                    if maybe_idx.isdigit():
                        idx = int(maybe_idx)
                except Exception:
                    idx = None
            # Parse timing
            timing = blk[timing_line_idx]
            parts = timing.split("-->")
            if len(parts) != 2:
                continue
            start_s = Transcript._parse_srt_timestamp(parts[0].strip())
            end_s = Transcript._parse_srt_timestamp(
                parts[1].strip().split()[0])
            # Remaining lines after timing are text, but if index consumed, skip it
            text_lines_start = timing_line_idx + 1
            lines = blk[text_lines_start:]
            text_payload = "\n".join(lines).strip()
            segments.append({
                "id": idx if isinstance(idx, int) else seq,
                "start": start_s,
                "end": end_s,
                "text": text_payload
            })
            seq += 1

        return json.dumps({"segments": segments}, ensure_ascii=False)

    @staticmethod
    def generate_srt_from_sjson(sjson_subs):
        import json
        if not isinstance(sjson_subs, str):
            raise TypeError("sjson_subs must be a string")
        try:
            data = json.loads(sjson_subs)
        except Exception as e:
            raise ValueError(f"Invalid JSON: {e}")
        segments = []
        if isinstance(data, dict) and "segments" in data and isinstance(data["segments"], list):
            segments = data["segments"]
        elif isinstance(data, list):
            segments = data
        else:
            raise ValueError(
                "SJSON must be an object with 'segments' list or a list of segments")

        # Normalize segments
        norm = []
        for i, seg in enumerate(segments, 1):
            if not isinstance(seg, dict):
                continue
            start = seg.get("start", 0)
            end = seg.get("end", start)
            text = seg.get("text", "")
            sid = seg.get("id", i)
            # Coerce to float
            try:
                start = float(start)
            except Exception:
                start = 0.0
            try:
                end = float(end)
            except Exception:
                end = start
            # Coerce text
            if not isinstance(text, str):
                text = str(text)
            # Coerce id
            try:
                sid = int(sid)
            except Exception:
                sid = i
            norm.append((sid, start, end, text))

        # Sort by id then start for deterministic order
        norm.sort(key=lambda t: (t[0], t[1]))

        lines = []
        for idx, start, end, text in norm:
            lines.append(str(idx))
            lines.append(
                f"{Transcript._format_srt_timestamp(start)} --> {Transcript._format_srt_timestamp(end)}")
            # Preserve multi-line text
            if text:
                lines.extend(text.split("\n"))
            lines.append("")  # blank line
        return "\n".join(lines).rstrip() + ("\n" if lines else "")

    @classmethod
    def convert(cls, content, input_format, output_format):
        fmt_in = (input_format or "").strip().lower()
        fmt_out = (output_format or "").strip().lower()
        if fmt_in == fmt_out:
            return content
        if fmt_in == "srt" and fmt_out in ("sjson", "json"):
            return cls.generate_sjson_from_srt(content)
        if fmt_in in ("sjson", "json") and fmt_out == "srt":
            return cls.generate_srt_from_sjson(content)
        raise ValueError(
            f"Unsupported conversion: {input_format} -> {output_format}")
