
from dataclasses import dataclass


@dataclass(init=False)
class StatusBioDTO:
    '''Status biography data transfer object'''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        '''Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        '''
        # Extract all attributes from the model that are not private
        attrs = {k: getattr(model, k)
                 for k in vars(model) if not k.startswith('_')}
        return cls(**attrs)

    def to_dict(self) -> dict:
        '''Return a dictionary representation of the DTO'''
        return {k: v for k, v in self.__dict__.items()}
