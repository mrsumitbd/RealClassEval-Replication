
class Transcript:

    @staticmethod
    def generate_sjson_from_srt(srt_subs):
        import re
        sjson_subs = []
        pattern = re.compile(
            r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\d+\n|\Z)', re.DOTALL)
        for match in pattern.finditer(srt_subs):
            index, start, end, text = match.groups()
            sjson_subs.append({
                "index": int(index),
                "start": start,
                "end": end,
                "text": text.strip()
            })
        return sjson_subs

    @staticmethod
    def generate_srt_from_sjson(sjson_subs):
        srt_subs = []
        for sub in sjson_subs:
            srt_subs.append(
                f"{sub['index']}\n{sub['start']} --> {sub['end']}\n{sub['text']}\n")
        return "\n".join(srt_subs)

    @classmethod
    def convert(cls, content, input_format, output_format):
        if input_format == 'srt' and output_format == 'sjson':
            return cls.generate_sjson_from_srt(content)
        elif input_format == 'sjson' and output_format == 'srt':
            return cls.generate_srt_from_sjson(content)
        else:
            raise ValueError("Unsupported format conversion")
