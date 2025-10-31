from pathlib import Path
from typing import List, Optional, Tuple

class MusicMetadata:
    """
    音乐元数据类.
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.filename = file_path.name
        self.file_id = file_path.stem
        self.file_size = file_path.stat().st_size
        self.title = None
        self.artist = None
        self.album = None
        self.duration = None

    def extract_metadata(self) -> bool:
        """
        提取音乐文件元数据.
        """
        if not MUTAGEN_AVAILABLE:
            return False
        try:
            audio_file = MutagenFile(self.file_path)
            if audio_file is None:
                return False
            if hasattr(audio_file, 'info'):
                self.duration = getattr(audio_file.info, 'length', None)
            tags = audio_file.tags if audio_file.tags else {}
            self.title = self._get_tag_value(tags, ['TIT2', 'TITLE', '©nam'])
            self.artist = self._get_tag_value(tags, ['TPE1', 'ARTIST', '©ART'])
            self.album = self._get_tag_value(tags, ['TALB', 'ALBUM', '©alb'])
            return True
        except ID3NoHeaderError:
            return True
        except Exception as e:
            logger.debug(f'提取元数据失败 {self.filename}: {e}')
            return False

    def _get_tag_value(self, tags: dict, tag_names: List[str]) -> Optional[str]:
        """
        从多个可能的标签名中获取值.
        """
        for tag_name in tag_names:
            if tag_name in tags:
                value = tags[tag_name]
                if isinstance(value, list) and value:
                    return str(value[0])
                elif value:
                    return str(value)
        return None

    def format_duration(self) -> str:
        """
        格式化播放时长.
        """
        if self.duration is None:
            return '未知'
        minutes = int(self.duration) // 60
        seconds = int(self.duration) % 60
        return f'{minutes:02d}:{seconds:02d}'