from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

class COLReader:

    def __init__(self, response):
        self.response = response
        self.items = self.response['items']
        data = []
        for item in self.items:
            id = item['contentDetails']['videoId']
            doc_url = ''.join(['https://www.youtube.com/watch?v=', item['contentDetails']['videoId']])
            date = datetime.strptime(item['contentDetails']['videoPublishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y%m%d')
            try:
                transcript = TextFormatter().format_transcript(YouTubeTranscriptApi.get_transcript(id, languages=['vi']))
            except Exception:
                print('Could not extract video: %s' % doc_url)
            if transcript:
                sentences = transcript.split('\n')
                for sentence in sentences:
                    if len(sentence.replace('♪', '').strip()):
                        s = {'doc_url': doc_url, 'date': date, 'sentence': sentence.replace('♪', '').strip()}
                        data.append(s)
        self.data = data

    def __len__(self):
        return len(self.items)