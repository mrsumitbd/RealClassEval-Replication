import time
import yaml
import hashlib
from typing import Dict
import os
import re

class WakeupWordsConfig:

    def __init__(self):
        self.config_file = 'data/.wakeup_words.yaml'
        self.assets_dir = 'config/assets/wakeup_words'
        self._ensure_directories()
        self._config_cache = None
        self._last_load_time = 0
        self._cache_ttl = 1
        self._lock_timeout = 5

    def _ensure_directories(self):
        """确保必要的目录存在"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        os.makedirs(self.assets_dir, exist_ok=True)

    def _load_config(self) -> Dict:
        """加载配置文件，使用缓存机制"""
        current_time = time.time()
        if self._config_cache is not None and current_time - self._last_load_time < self._cache_ttl:
            return self._config_cache
        try:
            with open(self.config_file, 'a+') as f:
                with FileLock(f, timeout=self._lock_timeout):
                    f.seek(0)
                    content = f.read()
                    config = yaml.safe_load(content) if content else {}
                    self._config_cache = config
                    self._last_load_time = current_time
                    return config
        except (TimeoutError, IOError) as e:
            print(f'加载配置文件失败: {e}')
            return {}
        except Exception as e:
            print(f'加载配置文件时发生未知错误: {e}')
            return {}

    def _save_config(self, config: Dict):
        """保存配置到文件，使用文件锁保护"""
        try:
            with open(self.config_file, 'w') as f:
                with FileLock(f, timeout=self._lock_timeout):
                    yaml.dump(config, f, allow_unicode=True)
                    self._config_cache = config
                    self._last_load_time = time.time()
        except (TimeoutError, IOError) as e:
            print(f'保存配置文件失败: {e}')
            raise
        except Exception as e:
            print(f'保存配置文件时发生未知错误: {e}')
            raise

    def get_wakeup_response(self, voice: str) -> Dict:
        voice = hashlib.md5(voice.encode()).hexdigest()
        '获取唤醒词回复配置'
        config = self._load_config()
        if not config or voice not in config:
            return None
        file_path = config[voice]['file_path']
        if not os.path.exists(file_path) or os.stat(file_path).st_size < 15 * 1024:
            return None
        return config[voice]

    def update_wakeup_response(self, voice: str, file_path: str, text: str):
        """更新唤醒词回复配置"""
        try:
            filtered_text = re.sub('[\\U0001F600-\\U0001F64F\\U0001F900-\\U0001F9FF]', '', text)
            config = self._load_config()
            voice_hash = hashlib.md5(voice.encode()).hexdigest()
            config[voice_hash] = {'voice': voice, 'file_path': file_path, 'time': time.time(), 'text': filtered_text}
            self._save_config(config)
        except Exception as e:
            print(f'更新唤醒词回复配置失败: {e}')
            raise

    def generate_file_path(self, voice: str) -> str:
        """生成音频文件路径，使用voice的哈希值作为文件名"""
        try:
            voice_hash = hashlib.md5(voice.encode()).hexdigest()
            file_path = os.path.join(self.assets_dir, f'{voice_hash}.wav')
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f'删除已存在的音频文件失败: {e}')
                    raise
            return file_path
        except Exception as e:
            print(f'生成音频文件路径失败: {e}')
            raise