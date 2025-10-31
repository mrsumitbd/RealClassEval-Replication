
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
        sjson_subs = {
            'start': [],
            'end': [],
            'text': []
        }
        for sub in srt_subs:
            sjson_subs['start'].append(sub.start.ordinal)
            sjson_subs['end'].append(sub.end.ordinal)
            sjson_subs['text'].append(sub.text)
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
        from pysrt import SubRipItem, SubRipTime
        srt_subs = []
        for i in range(len(sjson_subs['start'])):
            start = SubRipTime(milliseconds=sjson_subs['start'][i])
            end = SubRipTime(milliseconds=sjson_subs['end'][i])
            text = sjson_subs['text'][i]
            srt_subs.append(SubRipItem(start=start, end=end, text=text))
        return srt_subs

    @classmethod
    def convert(cls, content, input_format, output_format):
        if input_format == 'srt' and output_format == 'sjson':
            return cls.generate_sjson_from_srt(content)
        elif input_format == 'sjson' and output_format == 'srt':
            return cls.generate_srt_from_sjson(content)
        else:
            raise ValueError(
                f"Unsupported conversion: {input_format} to {output_format}")
