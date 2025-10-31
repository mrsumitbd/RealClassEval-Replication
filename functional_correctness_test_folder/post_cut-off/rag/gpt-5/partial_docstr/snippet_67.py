from dataclasses import dataclass, field, asdict
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    user_id: str
    amount: float
    duration: float  # 持续时间（秒）
    message: str = ''
    start_time: float = field(default_factory=time.time)

    def is_expired(self) -> bool:
        '''检查SuperChat是否已过期'''
        return self.remaining_time() <= 0.0

    def remaining_time(self) -> float:
        '''获取剩余时间（秒）'''
        end_time = self.start_time + max(0.0, self.duration)
        return max(0.0, end_time - time.time())

    def to_dict(self) -> dict:
        '''转换为字典格式'''
        data = asdict(self)
        data['remaining_time'] = self.remaining_time()
        data['expired'] = self.is_expired()
        return data
