
import json
import re


class Transcript:

    @staticmethod
    def generate_sjson_from_srt(srt_subs):
        """
        Generate sjson from srt subtitles.

        Args:
            srt_subs (str): The srt subtitles.

        Returns:
            str: The sjson subtitles.
        """
        sjson_subs = {"start": [], "end": [], "text": []}
        for block in srt_subs.split('\n\n'):
            if block.strip() == '':
                continue
            lines = block.split('\n')
            if len(lines) < 3:
                continue
            match = re.match(
                r'(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)', lines[1])
            if match:
                start_time = Transcript._srt_time_to_secs(match.group(1))
                end_time = Transcript._srt_time_to_secs(match.group(2))
                text = '\n'.join(lines[2:])
                sjson_subs["start"].append(start_time)
                sjson_subs["end"].append(end_time)
                sjson_subs["text"].append(text)
        return json.dumps(sjson_subs)

    @staticmethod
    def _srt_time_to_secs(time_str):
        """
        Convert srt time to seconds.

        Args:
            time_str (str): The time string in srt format.

        Returns:
            float: The time in seconds.
        """
        h, m, s = time_str.split(':')
        s, ms = s.split(',')
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    @staticmethod
    def _secs_to_srt_time(time_secs):
        """
        Convert seconds to srt time.

        Args:
            time_secs (float): The time in seconds.

        Returns:
            str: The time string in srt format.
        """
        h = int(time_secs // 3600)
        m = int((time_secs % 3600) // 60)
        s = int(time_secs % 60)
        ms = int((time_secs % 1) * 1000)
        return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

    @staticmethod
    def generate_srt_from_sjson(sjson_subs):
        """
        Generate srt from sjson subtitles.

        Args:
            sjson_subs (str): The sjson subtitles.

        Returns:
            str: The srt subtitles.
        """
        sjson_subs = json.loads(sjson_subs)
        srt_subs = ''
        for i in range(len(sjson_subs["start"])):
            srt_subs += f'{i+1}\n'
            srt_subs += f'{Transcript._secs_to_srt_time(sjson_subs["start"][i])} --> {Transcript._secs_to_srt_time(sjson_subs["end"][i])}\n'
            srt_subs += sjson_subs["text"][i] + '\n\n'
        return srt_subs.strip()

    @classmethod
    def convert(cls, content, input_format, output_format):
        """
        Convert subtitles from one format to another.

        Args:
            content (str): The subtitles content.
            input_format (str): The input format. Can be 'srt' or 'sjson'.
            output_format (str): The output format. Can be 'srt' or 'sjson'.

        Returns:
            str: The converted subtitles.

        Raises:
            ValueError: If the input or output format is not supported.
        """
        if input_format == 'srt' and output_format == 'sjson':
            return cls.generate_sjson_from_srt(content)
        elif input_format == 'sjson' and output_format == 'srt':
            return cls.generate_srt_from_sjson(content)
        else:
            raise ValueError('Unsupported format conversion')
