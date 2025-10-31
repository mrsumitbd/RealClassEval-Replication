class Transcript:
    '''
    Container for transcript methods.
    '''

    class TranscriptsGenerationException(Exception):
        pass

    @staticmethod
    def _parse_timestamp(ts):
        ts = ts.strip()
        # Expected format: HH:MM:SS,mmm
        try:
            hms, ms = ts.split(',')
            h, m, s = hms.split(':')
            total = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0
            return float(total)
        except Exception as e:
            raise ValueError(f"Invalid SRT timestamp: {ts}") from e

    @staticmethod
    def _format_timestamp(seconds):
        if seconds < 0:
            seconds = 0.0
        total_ms = int(round(seconds * 1000))
        ms = total_ms % 1000
        total_s = total_ms // 1000
        s = total_s % 60
        total_m = total_s // 60
        m = total_m % 60
        h = total_m // 60
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    @staticmethod
    def _ensure_text(s):
        if s is None:
            return ""
        return str(s)

    @staticmethod
    def _normalize_sjson(sjson_subs):
        # Accept dict {'segments': [...]}, or list directly
        if isinstance(sjson_subs, dict):
            if 'segments' in sjson_subs and isinstance(sjson_subs['segments'], list):
                return sjson_subs['segments']
            # Accept common alternatives
            for key in ('fragments', 'events', 'items', 'lines'):
                if key in sjson_subs and isinstance(sjson_subs[key], list):
                    return sjson_subs[key]
            # If dict looks like a single segment, wrap it
            if {'start', 'end', 'text'} & set(sjson_subs.keys()):
                return [sjson_subs]
            return []
        elif isinstance(sjson_subs, list):
            return sjson_subs
        else:
            return []

    @staticmethod
    def generate_sjson_from_srt(srt_subs):
        '''
        Generate transcripts from sjson to SubRip (*.srt).
        Arguments:
            srt_subs(SubRip): "SRT" subs object
        Returns:
            Subs converted to "SJSON" format.
        '''
        # Accept bytes, str, or any object with 'decode'
        if srt_subs is None:
            return {"segments": []}
        if isinstance(srt_subs, bytes):
            text = srt_subs.decode('utf-8', errors='replace')
        else:
            text = str(srt_subs)

        blocks = []
        # Normalize newlines
        text_norm = text.replace('\r\n', '\n').replace('\r', '\n')
        # Split into blocks separated by empty lines
        raw_blocks = [b for b in text_norm.split('\n\n') if b.strip() != '']
        for raw in raw_blocks:
            lines = [ln for ln in raw.split('\n') if ln.strip() != '']
            if not lines:
                continue
            # Detect if first line is an index
            time_line_idx = 0
            if '-->' not in lines[0]:
                # try next line
                if len(lines) < 2 or '-->' not in lines[1]:
                    # invalid block
                    raise Transcript.TranscriptsGenerationException(
                        "Invalid SRT block (missing time line)")
                time_line_idx = 1
            time_line = lines[time_line_idx].strip()
            if '-->' not in time_line:
                raise Transcript.TranscriptsGenerationException(
                    "Invalid SRT time line")
            parts = time_line.split('-->')
            if len(parts) != 2:
                raise Transcript.TranscriptsGenerationException(
                    "Invalid SRT time separator")
            start_str = parts[0].strip()
            end_str = parts[1].strip()
            try:
                start = Transcript._parse_timestamp(start_str)
                end = Transcript._parse_timestamp(end_str)
            except Exception as e:
                raise Transcript.TranscriptsGenerationException(
                    "Invalid SRT timestamps") from e
            if end < start:
                # Allow zero-duration but not negative
                end = start
            # Remaining lines after time line are text
            text_lines = lines[time_line_idx +
                               1:] if len(lines) > time_line_idx + 1 else []
            content = '\n'.join(text_lines)
            blocks.append({
                "start": start,
                "end": end,
                "duration": round(end - start, 3),
                "text": content
            })
        return {"segments": blocks}

    @staticmethod
    def generate_srt_from_sjson(sjson_subs):
        '''
        Generate transcripts from sjson to SubRip (*.srt)
        Arguments:
            sjson_subs (dict): `sjson` subs.
        Returns:
            Subtitles in SRT format.
        '''
        segments = Transcript._normalize_sjson(sjson_subs)
        srt_lines = []
        idx = 1
        for seg in segments:
            # Segment may be dict-like; tolerate missing keys
            start = None
            end = None
            text = ""
            if isinstance(seg, dict):
                text = Transcript._ensure_text(
                    seg.get('text') or seg.get('line') or seg.get('content') or "")
                if 'start' in seg:
                    try:
                        start = float(seg['start'])
                    except Exception:
                        start = 0.0
                if 'end' in seg:
                    try:
                        end = float(seg['end'])
                    except Exception:
                        end = None
                if end is None and 'duration' in seg and start is not None:
                    try:
                        end = float(start) + float(seg['duration'])
                    except Exception:
                        end = start
                if start is None and 'ts' in seg:
                    # Some schemas use 'ts' or 'time'
                    try:
                        start = float(seg['ts'])
                    except Exception:
                        start = 0.0
                if end is None and 'timeEnd' in seg:
                    try:
                        end = float(seg['timeEnd'])
                    except Exception:
                        end = start if start is not None else 0.0
            else:
                text = Transcript._ensure_text(seg)
                start = 0.0
                end = 0.0
            if start is None:
                start = 0.0
            if end is None:
                end = start
            if end < start:
                end = start
            srt_lines.append(str(idx))
            srt_lines.append(
                f"{Transcript._format_timestamp(start)} --> {Transcript._format_timestamp(end)}")
            # Ensure text lines do not contain CR
            srt_lines.extend(Transcript._ensure_text(text).replace(
                '\r\n', '\n').replace('\r', '\n').split('\n'))
            srt_lines.append("")  # blank line between blocks
            idx += 1
        return '\n'.join(srt_lines).rstrip() + ('\n' if srt_lines else '')

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
        if input_format not in ('sjson', 'srt'):
            raise ValueError("Unsupported input_format. Accepted: sjson, srt")
        if output_format not in ('sjson', 'srt'):
            raise ValueError("Unsupported output_format. Accepted: sjson, srt")

        # If same format, return as-is
        if input_format == output_format:
            return content

        # Normalize content
        data = content
        if isinstance(data, bytes):
            data_bytes = data
            data_text = data.decode('utf-8', errors='replace')
        else:
            data_bytes = None
            data_text = str(data) if data is not None else ""

        if input_format == 'srt' and output_format == 'sjson':
            try:
                sjson_obj = cls.generate_sjson_from_srt(data_text)
            except Transcript.TranscriptsGenerationException:
                raise
            except Exception as e:
                raise Transcript.TranscriptsGenerationException(
                    "Failed to parse SRT") from e
            try:
                import json
                return json.dumps(sjson_obj, ensure_ascii=False).encode('utf-8')
            except Exception as e:
                # Fallback safe serialization
                return str(sjson_obj).encode('utf-8')

        if input_format == 'sjson' and output_format == 'srt':
            # Parse JSON if bytes/string JSON
            sjson_obj = None
            if isinstance(content, (bytes, str)):
                try:
                    import json
                    sjson_obj = json.loads(data_text)
                except Exception:
                    # If not JSON decodable, attempt eval-safe fallback not used, default to empty
                    sjson_obj = {}
            elif isinstance(content, dict):
                sjson_obj = content
            else:
                sjson_obj = {}
            srt_str = cls.generate_srt_from_sjson(sjson_obj)
            return srt_str.encode('utf-8')

        # Should not reach here
        return content
