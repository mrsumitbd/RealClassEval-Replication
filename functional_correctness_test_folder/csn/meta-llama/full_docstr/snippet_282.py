
import json
from pysrt import SubRipFile, SubRipItem, SubRipTime


class TranscriptsGenerationException(Exception):
    pass


class Transcript:
    '''
    Container for transcript methods.
    '''
    @staticmethod
    def generate_sjson_from_srt(srt_subs):
        '''
        Generate transcripts from srt to SJSON.
        Arguments:
            srt_subs(SubRip): "SRT" subs object
        Returns:
            Subs converted to "SJSON" format.
        '''
        sjson_subs = []
        for sub in srt_subs:
            sjson_subs.append({
                'start': sub.start.ordinal,
                'end': sub.end.ordinal,
                'text': sub.text
            })
        return {'start': 0, 'end': srt_subs[-1].end.ordinal, 'subs': sjson_subs}

    @staticmethod
    def generate_srt_from_sjson(sjson_subs):
        '''
        Generate transcripts from sjson to SubRip (*.srt)
        Arguments:
            sjson_subs (dict): `sjson` subs.
        Returns:
            Subtitles in SRT format.
        '''
        srt_subs = SubRipFile()
        for idx, sub in enumerate(sjson_subs['subs']):
            item = SubRipItem(
                index=idx + 1,
                start=SubRipTime(milliseconds=sub['start']),
                end=SubRipTime(milliseconds=sub['end']),
                text=sub['text']
            )
            srt_subs.append(item)
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
        if input_format == 'sjson' and output_format == 'srt':
            sjson_subs = json.loads(content.decode('utf-8'))
            srt_subs = cls.generate_srt_from_sjson(sjson_subs)
            return srt_subs.to_string().encode('utf-8')
        elif input_format == 'srt' and output_format == 'sjson':
            try:
                srt_subs = SubRipFile.from_string(content.decode('utf-8'))
                sjson_subs = cls.generate_sjson_from_srt(srt_subs)
                return json.dumps(sjson_subs).encode('utf-8')
            except Exception as e:
                raise TranscriptsGenerationException(str(e))
        else:
            raise ValueError('Invalid input or output format')
