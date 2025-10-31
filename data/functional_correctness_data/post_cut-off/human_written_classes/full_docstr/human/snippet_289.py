from typing import Annotated, Any, Dict, Optional, Union
import json
from dataclasses import asdict, dataclass

@dataclass
class UpdateRuleDeployment:
    """Model for updating rule deployment."""
    enabled: Annotated[Optional[bool], 'Optional enabled flag of rule'] = None
    archived: Annotated[Optional[bool], 'Optional archived flag of rule'] = None
    detection_exclusion_application: Annotated[Optional[Union[str, Dict[str, Any]]], 'Optional detection exclusion application of rule'] = None

    def __post_init__(self):
        """Post initilizaiton for validating/converting attributes"""
        if self.enabled is True and self.archived is True:
            raise ValueError('enabled and archived flags cannot be true at same time')
        if isinstance(self.detection_exclusion_application, str):
            try:
                self.detection_exclusion_application = json.loads(self.detection_exclusion_application)
            except json.JSONDecodeError as e:
                raise ValueError(f'Invalid JSON string for detection_exclusion_application: {e}') from e

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)