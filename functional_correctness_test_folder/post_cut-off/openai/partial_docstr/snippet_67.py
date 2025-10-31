
from dataclasses import dataclass, asdict
import time


@dataclass
class SuperChatRecord:
    '''SuperChat记录数据类'''
    # 开始时间（Unix 时间戳，秒）
    start_time: float
    # 持续时间（秒）
    duration: float
    # 其它可选字段（可根据实际业务添加）
    user_id: int | None = None
    amount: float | None = None
    message: str | None = None

    def is_expired(self) -> bool:
        """判断 SuperChat 是否已过期"""
        return time.time() > self.start_time + self.duration

    def remaining_time(self) -> float:
        """获取剩余时间（秒）"""
        remaining = (self.start_time + self.duration) - time.time()
        return max(0.0, remaining)

    def to_dict(self) -> dict:
        """将记录转换为字典"""
        return asdict(self)
