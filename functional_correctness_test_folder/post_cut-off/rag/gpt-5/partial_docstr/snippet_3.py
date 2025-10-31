from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, Optional


@dataclass
class StatusBioDTO:
    '''Status biography data transfer object'''
    id: Optional[int] = None
    user_id: Optional[int] = None
    biography: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        '''Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        '''
        if model is None:
            return cls()

        # Extract raw data from the model
        data: Dict[str, Any] = {}

        # Prefer a to_dict-like method if present
        for method_name in ('to_dict', 'dict', 'as_dict'):
            if hasattr(model, method_name) and callable(getattr(model, method_name)):
                try:
                    maybe = getattr(model, method_name)()
                    if isinstance(maybe, dict):
                        data = maybe.copy()
                        break
                except Exception:
                    pass

        # Fallback: SQLAlchemy model with __table__.columns
        if not data and hasattr(model, '__table__') and hasattr(model.__table__, 'columns'):
            try:
                # type: ignore[attr-defined]
                col_names = [c.name for c in model.__table__.columns]
                data = {name: getattr(model, name, None) for name in col_names}
            except Exception:
                pass

        # Fallback: generic __dict__ filtering
        if not data:
            try:
                raw = getattr(model, '__dict__', {}) or {}
                data = {
                    k: v for k, v in raw.items()
                    if not k.startswith('_') and k != '_sa_instance_state'
                }
            except Exception:
                data = {}

        # Also handle case where model is already a dict-like object
        if not data and isinstance(model, dict):
            data = dict(model)

        # Normalize and map fields
        def pick(*keys, default=None):
            for k in keys:
                if k in data and data[k] is not None:
                    return data[k]
            return default

        dto = cls(
            id=pick('id', 'pk', 'bio_id'),
            user_id=pick('user_id', 'userId', 'account_id', 'owner_id'),
            biography=pick('biography', 'bio', 'status',
                           'about', 'text', 'description'),
            created_at=pick('created_at', 'createdAt',
                            'created', 'inserted_at', 'insertedAt'),
            updated_at=pick('updated_at', 'updatedAt',
                            'modified_at', 'modifiedAt', 'updated'),
        )

        # Collect remaining keys into extra
        known = {'id', 'user_id', 'biography', 'created_at', 'updated_at'}
        dto.extra = {k: v for k, v in data.items() if k not in known}

        return dto

    def to_dict(self) -> dict:
        '''Convert to dictionary format
        Returns:
            dict: dictionary format data
        '''
        def serialize(value: Any) -> Any:
            if isinstance(value, (datetime, date)):
                return value.isoformat()
            return value

        base = {
            'id': self.id,
            'user_id': self.user_id,
            'biography': self.biography,
            'created_at': serialize(self.created_at),
            'updated_at': serialize(self.updated_at),
        }

        # Merge extras, without overriding base fields
        result = {**self.extra, **{k: v for k,
                                   v in base.items() if v is not None}}
        return result
