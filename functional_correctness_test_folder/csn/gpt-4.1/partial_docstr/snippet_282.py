
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
                "index": sub['index'],
                "start": sub['start'],
                "end": sub['end'],
                "text": sub['text']
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
        lines = []
        for entry in sjson_subs.get("transcript", []):
            lines.append(str(entry["index"]))
            lines.append(f"{entry['start']} --> {entry['end']}")
            lines.append(entry["text"])
            lines.append("")  # blank line between subs
        return "\n".join(lines).strip()

    @classmethod
    def convert(cls, content, input_format, output_format):
        if input_format == "srt" and output_format == "sjson":
            # Parse SRT string to list of dicts
            srt_subs = []
            blocks = content.strip().split('\n\n')
            for block in blocks:
                lines = block.strip().split('\n')
                if len(lines) >= 3:
                    index = int(lines[0])
                    times = lines[1]
                    start, end = times.split(' --> ')
                    text = "\n".join(lines[2:])
                    srt_subs.append({
                        "index": index,
                        "start": start.strip(),
                        "end": end.strip(),
                        "text": text
                    })
            return cls.generate_sjson_from_srt(srt_subs)
        elif input_format == "sjson" and output_format == "srt":
            return cls.generate_srt_from_sjson(content)
        else:
            raise ValueError("Unsupported conversion: {} to {}".format(
                input_format, output_format))
