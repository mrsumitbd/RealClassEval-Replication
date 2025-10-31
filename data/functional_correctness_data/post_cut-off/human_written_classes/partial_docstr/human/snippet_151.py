from typing import Dict, Any
import uuid
from typing import Optional, Literal
import os
import subprocess
import json

class Audio_material:
    """本地音频素材"""
    material_id: str
    '素材全局id, 自动生成'
    material_name: str
    '素材名称'
    path: str
    '素材文件路径'
    remote_url: Optional[str] = None
    '远程URL地址'
    replace_path: Optional[str] = None
    '替换路径, 如果设置了这个值, 在导出json时会用这个路径替代原始path'
    has_audio_effect: bool = False
    '是否有音频效果'
    duration: int
    '素材时长, 单位为微秒'

    def __init__(self, path: Optional[str]=None, replace_path=None, material_name: Optional[str]=None, remote_url: Optional[str]=None, duration: Optional[float]=None):
        """从指定位置加载音频素材, 注意视频文件不应该作为音频素材使用

        Args:
            path (`str`, optional): 素材文件路径, 支持mp3, wav等常见音频文件.
            material_name (`str`, optional): 素材名称, 如果不指定, 默认使用URL中的文件名作为素材名称.
            remote_url (`str`, optional): 远程URL地址.
            duration (`float`, optional): 音频时长（秒），如果提供则跳过ffprobe检测.

        Raises:
            `ValueError`: 不支持的素材文件类型或缺少必要参数.
        """
        if not path and (not remote_url):
            raise ValueError('必须提供 path 或 remote_url 中的至少一个参数')
        if path:
            path = os.path.abspath(path)
            if not os.path.exists(path):
                raise FileNotFoundError(f'找不到 {path}')
        if not material_name and remote_url:
            original_filename = os.path.basename(remote_url.split('?')[0])
            name_without_ext = os.path.splitext(original_filename)[0]
            material_name = f'{name_without_ext}.mp3'
        self.material_name = material_name if material_name else os.path.basename(path) if path else 'unknown'
        self.material_id = uuid.uuid3(uuid.NAMESPACE_DNS, self.material_name).hex
        self.path = path if path else ''
        self.replace_path = replace_path
        self.remote_url = remote_url
        if duration is not None:
            self.duration = int(float(duration) * 1000000.0)
            return
        self.duration = 0
        try:
            command = ['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=duration', '-show_entries', 'format=duration', '-of', 'json', path if path else remote_url]
            result = subprocess.check_output(command, stderr=subprocess.STDOUT)
            result_str = result.decode('utf-8')
            json_start = result_str.find('{')
            if json_start != -1:
                json_str = result_str[json_start:]
                info = json.loads(json_str)
            else:
                raise ValueError(f'无法在输出中找到JSON数据: {result_str}')
            video_command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_type', '-of', 'json', path if path else remote_url]
            video_result = subprocess.check_output(video_command, stderr=subprocess.STDOUT)
            video_result_str = video_result.decode('utf-8')
            video_json_start = video_result_str.find('{')
            if video_json_start != -1:
                video_json_str = video_result_str[video_json_start:]
                video_info = json.loads(video_json_str)
            else:
                print(f'无法在输出中找到JSON数据: {video_result_str}')
            if 'streams' in video_info and len(video_info['streams']) > 0:
                raise ValueError('音频素材不应包含视频轨道')
            if 'streams' in info and len(info['streams']) > 0:
                stream = info['streams'][0]
                duration_value = stream.get('duration') or info['format'].get('duration', '0')
                self.duration = int(float(duration_value) * 1000000.0)
            else:
                raise ValueError(f'给定的素材文件 {path} 没有音频轨道')
        except subprocess.CalledProcessError as e:
            raise ValueError(f"处理文件 {path} 时出错: {e.output.decode('utf-8')}")
        except json.JSONDecodeError as e:
            raise ValueError(f'解析媒体信息时出错: {e}')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Audio_material':
        """从字典创建音频素材对象

        Args:
            data (Dict[str, Any]): 包含素材信息的字典

        Returns:
            Audio_material: 新创建的音频素材对象
        """
        instance = cls.__new__(cls)
        instance.material_id = data['id']
        instance.material_name = data['name']
        instance.path = data['path']
        instance.duration = data['duration']
        instance.replace_path = None
        instance.remote_url = data.get('remote_url')
        return instance

    def export_json(self) -> Dict[str, Any]:
        return {'app_id': 0, 'category_id': '', 'category_name': 'local', 'check_flag': 3 if hasattr(self, 'has_audio_effect') and self.has_audio_effect else 1, 'copyright_limit_type': 'none', 'duration': self.duration, 'effect_id': '', 'formula_id': '', 'id': self.material_id, 'intensifies_path': '', 'is_ai_clone_tone': False, 'is_text_edit_overdub': False, 'is_ugc': False, 'local_material_id': self.material_id, 'music_id': self.material_id, 'name': self.material_name, 'path': self.replace_path if self.replace_path is not None else self.path, 'remote_url': self.remote_url, 'query': '', 'request_id': '', 'resource_id': '', 'search_id': '', 'source_from': '', 'source_platform': 0, 'team_id': '', 'text_id': '', 'tone_category_id': '', 'tone_category_name': '', 'tone_effect_id': '', 'tone_effect_name': '', 'tone_platform': '', 'tone_second_category_id': '', 'tone_second_category_name': '', 'tone_speaker': '', 'tone_type': '', 'type': 'extract_music', 'video_id': '', 'wave_points': []}