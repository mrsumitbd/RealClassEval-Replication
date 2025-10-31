
import re


class Transcript:

    @staticmethod
    def generate_sjson_from_srt(srt_subs):
        def srt_time_to_seconds(t):
            h, m, s = t.replace(',', ':').split(':')
            return float(h) * 3600 + float(m) * 60 + float(s)

        entries = []
        pattern = re.compile(
            r'(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s+([\s\S]+?)(?=\n\d+\n|\Z)', re.MULTILINE)
        for match in pattern.finditer(srt_subs.strip()):
            idx, start, end, text = match.groups()
            text = text.strip().replace('\n', ' ')
            entries.append({
                "start": srt_time_to_seconds(start),
                "end": srt_time_to_seconds(end),
                "text": text
            })
        return entries

    @staticmethod
    def generate_srt_from_sjson(sjson_subs):
        def seconds_to_srt_time(seconds):
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            ms = int(round((seconds - int(seconds)) * 1000))
            return f"{h:02}:{m:02}:{s:02},{ms:03}"

        srt_lines = []
        for idx, entry in enumerate(sjson_subs, 1):
            start = seconds_to_srt_time(entry['start'])
            end = seconds_to_srt_time(entry['end'])
            text = entry['text']
            srt_lines.append(f"{idx}\n{start} --> {end}\n{text}\n")
        return '\n'.join(srt_lines).strip()

    @classmethod
    def convert(cls, content, input_format, output_format):
        if input_format == 'srt' and output_format == 'sjson':
            return cls.generate_sjson_from_srt(content)
        elif input_format == 'sjson' and output_format == 'srt':
            return cls.generate_srt_from_sjson(content)
        elif input_format == output_format:
            return content
        else:
            raise ValueError("Unsupported conversion")
