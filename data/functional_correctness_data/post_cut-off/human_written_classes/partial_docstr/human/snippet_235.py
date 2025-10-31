from typing import Dict, List, Optional
import hashlib
from datetime import datetime
from pathlib import Path

class MusicMetadata:
    """
    音乐元数据类.
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.filename = file_path.name
        self.file_id = file_path.stem
        self.file_size = file_path.stat().st_size
        self.creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
        self.modification_time = datetime.fromtimestamp(file_path.stat().st_mtime)
        self.title = None
        self.artist = None
        self.album = None
        self.genre = None
        self.year = None
        self.duration = None
        self.bitrate = None
        self.sample_rate = None
        self.file_hash = self._calculate_hash()

    def _calculate_hash(self) -> str:
        """
        计算文件MD5哈希值（仅前1MB避免大文件计算过慢）
        """
        try:
            hash_md5 = hashlib.md5()
            with open(self.file_path, 'rb') as f:
                chunk = f.read(1024 * 1024)
                hash_md5.update(chunk)
            return hash_md5.hexdigest()[:16]
        except Exception:
            return 'unknown'

    def extract_metadata(self) -> bool:
        """
        提取音乐文件元数据.
        """
        try:
            audio_file = MutagenFile(self.file_path)
            if audio_file is None:
                return False
            if hasattr(audio_file, 'info'):
                self.duration = getattr(audio_file.info, 'length', None)
                self.bitrate = getattr(audio_file.info, 'bitrate', None)
                self.sample_rate = getattr(audio_file.info, 'sample_rate', None)
            tags = audio_file.tags if audio_file.tags else {}
            self.title = self._get_tag_value(tags, ['TIT2', 'TITLE', '©nam'])
            self.artist = self._get_tag_value(tags, ['TPE1', 'ARTIST', '©ART'])
            self.album = self._get_tag_value(tags, ['TALB', 'ALBUM', '©alb'])
            self.genre = self._get_tag_value(tags, ['TCON', 'GENRE', '©gen'])
            year_raw = self._get_tag_value(tags, ['TDRC', 'DATE', 'YEAR', '©day'])
            if year_raw:
                year_str = str(year_raw)
                if year_str.isdigit():
                    self.year = int(year_str)
                else:
                    import re
                    year_match = re.search('(\\d{4})', year_str)
                    if year_match:
                        self.year = int(year_match.group(1))
            return True
        except ID3NoHeaderError:
            return True
        except Exception as e:
            print(f'提取元数据失败 {self.filename}: {e}')
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

    def format_file_size(self) -> str:
        """
        格式化文件大小.
        """
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f'{size:.1f} {unit}'
            size /= 1024.0
        return f'{size:.1f} TB'

    def to_dict(self) -> Dict:
        """
        转换为字典格式.
        """
        return {'file_id': self.file_id, 'filename': self.filename, 'title': self.title, 'artist': self.artist, 'album': self.album, 'genre': self.genre, 'year': self.year, 'duration': self.duration, 'duration_formatted': self.format_duration(), 'bitrate': self.bitrate, 'sample_rate': self.sample_rate, 'file_size': self.file_size, 'file_size_formatted': self.format_file_size(), 'file_hash': self.file_hash, 'creation_time': self.creation_time.isoformat(), 'modification_time': self.modification_time.isoformat()}