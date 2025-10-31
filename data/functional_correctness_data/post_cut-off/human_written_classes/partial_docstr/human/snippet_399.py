import shutil
import torch
from cosmos_rl.utils.logging import logger
import os
from typing import Optional, Any
from concurrent.futures import ThreadPoolExecutor

class DiskCache:
    """use disk cache datasets's preprocess data"""

    def __init__(self, cache_path: str):
        self.cache_path = cache_path
        os.makedirs(self.cache_path, exist_ok=True)
        self.max_concurrent_tasks = 4
        self.max_files_per_dir = 10000
        self.executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix='disk_cache')

    def __cache_ojb_path(self, idx: int) -> str:
        subdir = str(idx // self.max_files_per_dir)
        subdir_path = os.path.join(self.cache_path, subdir)
        os.makedirs(subdir_path, exist_ok=True)
        return os.path.join(subdir_path, f'{idx}.pt')

    def __save_to_disk(self, path: str, obj: Any) -> None:

        def save_obj_helper(obj, path):
            tmp_file = f'{path}.tmp'
            try:
                torch.save(obj, tmp_file)
                os.rename(tmp_file, path)
            except Exception:
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)
        self.executor.submit(save_obj_helper, obj, path)

    def set(self, idx: int, obj: Any) -> None:
        if self.executor._work_queue.qsize() > self.max_concurrent_tasks:
            return
        cachePath = self.__cache_ojb_path(idx)
        self.__save_to_disk(cachePath, obj)

    def get(self, idx: int) -> Optional[Any]:
        cachePath = self.__cache_ojb_path(idx)
        if os.path.exists(cachePath):
            try:
                return torch.load(cachePath)
            except Exception as e:
                logger.error(f'Failed to load cache file {cachePath}: {e}')
                return None
        return None

    def clear(self) -> None:
        self.executor.shutdown(wait=False)
        if os.path.exists(self.cache_path):
            shutil.rmtree(self.cache_path)