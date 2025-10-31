from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class StatusBioDTO:
    '''Status biography data transfer object'''
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        '''Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        '''
        if model is None:
            raise ValueError('model must not be None')

        # Preferred: model has its own serializer
        if hasattr(model, 'to_dict') and callable(getattr(model, 'to_dict')):
            data = model.to_dict()  # type: ignore[assignment]
            if not isinstance(data, dict):
                data = dict(data)
            return cls(data=data)

        # SQLAlchemy model with __table__.columns
        if hasattr(model, '__table__') and hasattr(model.__table__, 'columns'):
            try:
                # type: ignore[attr-defined]
                columns = getattr(model.__table__, 'columns')
                data = {col.name: getattr(model, col.name) for col in columns}
                return cls(data=data)
            except Exception:
                pass

        # SQLAlchemy model with __mapper__.attrs
        if hasattr(model, '__mapper__') and hasattr(model.__mapper__, 'attrs'):
            try:
                # type: ignore[attr-defined]
                attrs = getattr(model.__mapper__, 'attrs')
                data = {attr.key: getattr(model, attr.key) for attr in attrs}
                return cls(data=data)
            except Exception:
                pass

        # Django model
        if hasattr(model, '_meta') and hasattr(model._meta, 'fields'):
            try:
                fields = getattr(model._meta, 'fields')
                data = {f.name: getattr(model, f.name) for f in fields}
                return cls(data=data)
            except Exception:
                pass

        # Fallback: public attributes
        try:
            raw = vars(model)
        except TypeError:
            raw = model.__dict__ if hasattr(model, '__dict__') else {}
        data = {k: v for k, v in raw.items() if not k.startswith('_')}
        return cls(data=data)

    def to_dict(self) -> dict:
        '''Convert to dictionary format
        Returns:
            dict: dictionary format data
        '''
        return dict(self.data)
