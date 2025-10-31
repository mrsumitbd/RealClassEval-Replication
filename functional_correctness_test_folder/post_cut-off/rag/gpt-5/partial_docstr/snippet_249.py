from typing import Dict


class Message:
    '''消息类'''

    VALID_ROLES = {'system', 'user', 'assistant'}

    def __init__(self, role: str, content: str):
        '''
        初始化消息
        Args:
            role: 消息角色（"system", "user", "assistant"）
            content: 消息内容
        '''
        if not isinstance(role, str):
            raise TypeError('role must be a string')
        normalized_role = role.strip().lower()
        if normalized_role not in self.VALID_ROLES:
            raise ValueError(f'role must be one of {self.VALID_ROLES}')
        if not isinstance(content, str):
            raise TypeError('content must be a string')
        self.role = normalized_role
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        '''转换为字典格式'''
        return {'role': self.role, 'content': self.content}

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Message':
        '''从字典创建消息'''
        if not isinstance(data, dict):
            raise TypeError('data must be a dict')
        if 'role' not in data or 'content' not in data:
            raise ValueError('data must contain "role" and "content" keys')
        return cls(role=data['role'], content=data['content'])
