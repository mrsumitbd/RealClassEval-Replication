
import json
from babelfish import Language
from pysrt import SubRipFile, SubRipItem, error as srt_error


class TranscriptsGenerationException(Exception):
    pass


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
        for sub in srt_subs:
            sjson_subs.append({
                'index': sub.index,
                'start': {'seconds': sub.start.ordinal / 1000.0},
                'end': {'seconds': sub.end.ordinal / 1000.0},
                'text': sub.text
            })
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
        srt_subs = SubRipFile()
        for sub in sjson_subs:
            start_time = sub['start']['seconds'] * 1000
            end_time = sub['end']['seconds'] * 1000
            srt_item = SubRipItem(
                index=sub['index'],
                start=SubRipItem.to_time(start_time),
                end=SubRipItem.to_time(end_time),
                text=sub['text']
            )
            srt_subs.append(srt_item)
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
                srt_subs = SubRipFile.from_string(content.decode('utf-8'))
                return cls.generate_sjson_from_srt(srt_subs)
            except srt_error.Error as e:
                raise TranscriptsGenerationException(
                    f"Error parsing SRT content: {e}")
        elif input_format == 'sjson' and output_format == 'srt':
            try:
                sjson_subs = json.loads(content.decode('utf-8'))
                srt_subs = cls.generate_srt_from_sjson(sjson_subs)
                return srt_subs.to_string().encode('utf-8')
            except (json.JSONDecodeError, KeyError) as e:
                raise TranscriptsGenerationException(
                    f"Error parsing SJSON content: {e}")
        else:
            raise ValueError("Unsupported format conversion")
