
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
        sjson_subs = []
        for i, sub in enumerate(srt_subs):
            sjson_sub = {
                'id': i + 1,
                'start': sub.start.total_seconds(),
                'end': sub.end.total_seconds(),
                'text': sub.text
            }
            sjson_subs.append(sjson_sub)
        return sjson_subs

    @staticmethod
    def generate_srt_from_sjson(sjson_subs):
        '''
        Generate transcripts from sjson to SubRip (*.srt)
        Arguments:
            sjson_subs (dict): `sjson` subs.
        Returns:
            Subtitles in SRT format.
        '''
        srt_subs = []
        for sub in sjson_subs:
            srt_sub = {
                'index': sub['id'],
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
