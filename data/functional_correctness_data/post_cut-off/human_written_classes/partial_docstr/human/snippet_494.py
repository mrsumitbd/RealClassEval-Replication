from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class API:
    """
    Represents an API definition within API Management.
    """
    name: str
    displayName: str
    path: str
    description: str
    policyXml: Optional[str] = None
    operations: Optional[List['APIOperation']] = None
    tags: Optional[List[str]] = None
    productNames: Optional[List[str]] = None
    subscriptionRequired: bool = True
    serviceUrl: Optional[str] = None

    def __init__(self, name: str, displayName: str, path: str, description: str, policyXml: Optional[str]=None, operations: Optional[List['APIOperation']]=None, tags: Optional[List[str]]=None, productNames: Optional[List[str]]=None, subscriptionRequired: bool=True, serviceUrl: Optional[str]=None):
        self.name = name
        self.displayName = displayName
        self.path = path
        self.description = description
        self.policyXml = policyXml if policyXml is not None else _read_policy_xml(DEFAULT_XML_POLICY_PATH)
        self.operations = operations if operations is not None else []
        self.tags = tags if tags is not None else []
        self.productNames = productNames if productNames is not None else []
        self.serviceUrl = serviceUrl
        self.subscriptionRequired = subscriptionRequired

    def to_dict(self) -> dict:
        return {'name': self.name, 'displayName': self.displayName, 'path': self.path, 'description': self.description, 'operations': [op.to_dict() for op in self.operations] if self.operations else [], 'serviceUrl': self.serviceUrl, 'subscriptionRequired': self.subscriptionRequired, 'policyXml': self.policyXml, 'tags': self.tags, 'productNames': self.productNames}