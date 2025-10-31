
import json
from pysrt import SubRipItem, SubRipFile


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
                'start': {'hours': sub.start.hours, 'minutes': sub.start.minutes, 'seconds': sub.start.seconds, 'milliseconds': sub.start.milliseconds},
                'end': {'hours': sub.end.hours, 'minutes': sub.end.minutes, 'seconds': sub.end.seconds, 'milliseconds': sub.end.milliseconds},
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
            start = SubRipItem.Time(sub['start']['hours'], sub['start']['minutes'],
                                    sub['start']['seconds'], sub['start']['milliseconds'])
            end = SubRipItem.Time(sub['end']['hours'], sub['end']['minutes'],
                                  sub['end']['seconds'], sub['end']['milliseconds'])
            srt_sub = SubRipItem(
                index=sub['index'], start=start, end=end, text=sub['text'])
            srt_subs.append(srt_sub)
        return srt_subs

    @classmethod
    def convert(cls, content, input_format, output_format):
        if input_format == 'srt' and output_format == 'sjson':
            srt_subs = SubRipFile.from_string(content)
            return cls.generate_sjson_from_srt(srt_subs)
        elif input_format == 'sjson' and output_format == 'srt':
            sjson_subs = json.loads(content)
            srt_subs = cls.generate_srt_from_sjson(sjson_subs)
            return str(srt_subs)
        else:
            raise ValueError("Unsupported format conversion")
