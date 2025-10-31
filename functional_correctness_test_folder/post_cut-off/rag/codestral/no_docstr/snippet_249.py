
from typing import Dict


class Message:
    '''消息类'''

    def __init__(self, role: str, content: str):
        '''
        初始化消息
        Args:
            role: 消息角色（"system", "user", "assistant"）
            content: 消息内容
        '''
        self.role = role
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        '''转换为字典格式'''
        return {
            'role': self.role,
            'content': self.content
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Message':
        '''从字典创建消息'''
        return cls(data['role'], data['content'])
