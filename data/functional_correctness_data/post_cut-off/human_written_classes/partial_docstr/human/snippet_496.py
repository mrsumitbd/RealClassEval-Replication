from dataclasses import dataclass

@dataclass
class PolicyFragment:
    """
    Represents a policy fragment within API Management.
    """
    name: str
    policyXml: str
    description: str

    def __init__(self, name: str, policyXml: str, description: str='') -> None:
        self.name = name
        self.policyXml = policyXml
        self.description = description

    def to_dict(self) -> dict:
        pf_dict = {'name': self.name, 'policyXml': self.policyXml, 'description': self.description}
        return pf_dict