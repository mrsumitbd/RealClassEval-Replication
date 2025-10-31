
from dataclasses import dataclass
from typing import Dict, Any
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        pass

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        pass

    def to_dict(self) -> Dict[str, Any]:
        '''转换为字典格式'''
        pass
