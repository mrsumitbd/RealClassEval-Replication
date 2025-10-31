
class Transcript:

    @staticmethod
    def generate_sjson_from_srt(srt_subs):

        sjson_subs = []
        for sub in srt_subs:
            sjson_sub = {
                'start': sub.start.total_seconds(),
                'end': sub.end.total_seconds(),
                'text': sub.content
            }
            sjson_subs.append(sjson_sub)
        return sjson_subs

    @staticmethod
    def generate_srt_from_sjson(sjson_subs):

        srt_subs = []
        for sub in sjson_subs:
            srt_sub = {
                'start': sub['start'],
                'end': sub['end'],
                'text': sub['text']
            }
            srt_subs.append(srt_sub)
        return srt_subs

    @classmethod
    def convert(cls, content, input_format, output_format):

        if input_format == 'srt' and output_format == 'sjson':
            return cls.generate_sjson_from_srt(content)
        elif input_format == 'sjson' and output_format == 'srt':
            return cls.generate_srt_from_sjson(content)
        else:
            raise ValueError("Unsupported conversion format")
