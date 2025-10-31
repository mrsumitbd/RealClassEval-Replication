from typing import Dict


class Message:
    '''消息类'''

    _ALLOWED_ROLES = {"system", "user", "assistant"}

    def __init__(self, role: str, content: str):
        '''
        初始化消息
        Args:
            role: 消息角色（"system", "user", "assistant"）
            content: 消息内容
        '''
        if not isinstance(role, str):
            raise TypeError("role 必须为字符串")
        role = role.strip()
        if role not in self._ALLOWED_ROLES:
            raise ValueError(f'无效的 role: {role}，必须是 {self._ALLOWED_ROLES}')
        if not isinstance(content, str):
            raise TypeError("content 必须为字符串")

        self.role = role
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        '''转换为字典格式'''
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Message':
        '''从字典创建消息'''
        if data is None:
            raise ValueError("data 不能为空")
        if not isinstance(data, dict):
            raise TypeError("data 必须为字典")
        if "role" not in data or "content" not in data:
            raise ValueError('data 必须包含 "role" 与 "content" 键')
        return cls(role=data["role"], content=data["content"])
