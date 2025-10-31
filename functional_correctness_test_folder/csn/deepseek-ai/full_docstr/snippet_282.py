
import json
from webvtt import WebVTT, Caption
from io import StringIO


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
        sjson = {
            'start': [],
            'end': [],
            'text': []
        }
        for caption in srt_subs:
            sjson['start'].append(caption.start_in_seconds)
            sjson['end'].append(caption.end_in_seconds)
            sjson['text'].append(caption.text)
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
        srt_subs = WebVTT()
        for start, end, text in zip(sjson_subs['start'], sjson_subs['end'], sjson_subs['text']):
            caption = Caption(
                start,
                end,
                text
            )
            srt_subs.captions.append(caption)
        buffer = StringIO()
        srt_subs.write(buffer)
        return buffer.getvalue()

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
                srt_subs = WebVTT.read(content)
                return cls.generate_sjson_from_srt(srt_subs)
            except Exception as e:
                raise TranscriptsGenerationException(
                    f"Failed to parse SRT content: {str(e)}")
        elif input_format == 'sjson' and output_format == 'srt':
            sjson_subs = json.loads(content)
            return cls.generate_srt_from_sjson(sjson_subs)
        else:
            raise ValueError(
                f"Unsupported conversion from {input_format} to {output_format}")


class TranscriptsGenerationException(Exception):
    pass
