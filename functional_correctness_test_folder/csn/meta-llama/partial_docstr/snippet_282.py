
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
            start_time = sub.start.total_seconds()
            end_time = sub.end.total_seconds()
            sjson_subs.append({
                'start_time': start_time,
                'end_time': end_time,
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
        srt_subs = ''
        for index, sub in enumerate(sjson_subs, start=1):
            start_time = Transcript._format_time(sub['start_time'])
            end_time = Transcript._format_time(sub['end_time'])
            text = sub['text'].replace('\n', ' ')
            srt_subs += f'{index}\n{start_time} --> {end_time}\n{text}\n\n'
        return srt_subs.strip()

    @staticmethod
    def _format_time(total_seconds):
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds % 1) * 1000)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}'

    @classmethod
    def convert(cls, content, input_format, output_format):
        if input_format.lower() == 'srt' and output_format.lower() == 'sjson':
            from pysrt import SubRipFile
            srt_subs = SubRipFile.from_string(content)
            return cls.generate_sjson_from_srt(srt_subs)
        elif input_format.lower() == 'sjson' and output_format.lower() == 'srt':
            import json
            sjson_subs = json.loads(content)
            return cls.generate_srt_from_sjson(sjson_subs)
        else:
            raise ValueError('Unsupported format conversion')
