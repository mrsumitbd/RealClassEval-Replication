from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Tag:
    key: str
    value: Optional[str] = None
    id: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        '''Convert the tag to a dictionary for API requests'''
        data = {'key': self.key}
        if self.value is not None:
            data['value'] = self.value
        if self.id is not None:
            data['id'] = self.id
        if self.color is not None:
            data['color'] = self.color
        if self.description is not None:
            data['description'] = self.description
        if self.extra:
            data.update(self.extra)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        '''Create a Tag instance from API response data'''
        if not isinstance(data, dict):
            raise TypeError('data must be a dict')

        key = data.get('key', data.get('name'))
        if key is None:
            raise ValueError('Tag requires a "key" (or "name") field')

        value = data.get('value')
        id_ = data.get('id')
        color = data.get('color')
        description = data.get('description')

        known = {'key', 'name', 'value', 'id', 'color', 'description'}
        extra = {k: v for k, v in data.items() if k not in known}

        return cls(
            key=key,
            value=value,
            id=id_,
            color=color,
            description=description,
            extra=extra
        )
