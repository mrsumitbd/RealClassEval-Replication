
class Transcript:

    @staticmethod
    def generate_sjson_from_srt(srt_subs):
        lines = srt_subs.strip().split('\n')
        sjson = []
        i = 0
        while i < len(lines):
            if lines[i].strip().isdigit():
                index = int(lines[i])
                i += 1
                time_line = lines[i].strip()
                start, end = time_line.split(' --> ')
                i += 1
                text_lines = []
                while i < len(lines) and lines[i].strip() != '':
                    text_lines.append(lines[i].strip())
                    i += 1
                text = ' '.join(text_lines)
                sjson.append({
                    'start': start.strip(),
                    'end': end.strip(),
                    'text': text
                })
            else:
                i += 1
        return sjson

    @staticmethod
    def generate_srt_from_sjson(sjson_subs):
        srt = []
        for idx, sub in enumerate(sjson_subs, 1):
            srt.append(
                f"{idx}\n{sub['start']} --> {sub['end']}\n{sub['text']}\n")
        return '\n'.join(srt)

    @classmethod
    def convert(cls, content, input_format, output_format):
        if input_format == 'srt' and output_format == 'sjson':
            return cls.generate_sjson_from_srt(content)
        elif input_format == 'sjson' and output_format == 'srt':
            return cls.generate_srt_from_sjson(content)
        else:
            raise ValueError("Unsupported conversion")
