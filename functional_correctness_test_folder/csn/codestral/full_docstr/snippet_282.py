
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
        for i, sub in enumerate(sjson_subs):
            srt_sub = {
                'index': i + 1,
                'start': sub['start'],
                'end': sub['end'],
                'text': sub['text']
            }
            srt_subs.append(srt_sub)
        return srt_subs

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
        if input_format == 'srt' and output_format == 'sjson':
            try:
                srt_subs = SubRip(content)
                return cls.generate_sjson_from_srt(srt_subs)
            except Exception as e:
                raise TranscriptsGenerationException(
                    f"Error parsing SRT content: {e}")
        elif input_format == 'sjson' and output_format == 'srt':
            sjson_subs = json.loads(content)
            return cls.generate_srt_from_sjson(sjson_subs)
        else:
            raise ValueError(
                f"Unsupported conversion from {input_format} to {output_format}")
