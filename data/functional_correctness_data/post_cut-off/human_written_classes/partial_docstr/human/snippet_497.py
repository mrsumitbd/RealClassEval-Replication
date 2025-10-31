from typing import List, Optional, Any
from dataclasses import dataclass

@dataclass
class Product:
    """
    Represents a Product definition within API Management.
    Products in APIM are logical groupings of APIs with associated policies,
    terms of use, and rate limits. They are used to manage API access control.
    """
    name: str
    displayName: str
    description: str
    state: str = 'published'
    subscriptionRequired: bool = True
    approvalRequired: bool = False
    policyXml: Optional[str] = None

    def __init__(self, name: str, displayName: str, description: str, state: str='published', subscriptionRequired: bool=True, approvalRequired: bool=False, policyXml: Optional[str]=None) -> None:
        self.name = name
        self.displayName = displayName
        self.description = description
        self.state = state
        self.subscriptionRequired = subscriptionRequired
        self.approvalRequired = approvalRequired
        if policyXml is None:
            try:
                self.policyXml = _read_policy_xml(DEFAULT_XML_POLICY_PATH)
            except FileNotFoundError:
                self.policyXml = '<policies>\n    <inbound>\n        <base />\n    </inbound>\n    <backend>\n        <base />\n    </backend>\n    <outbound>\n        <base />\n    </outbound>\n    <on-error>\n        <base />\n    </on-error>\n</policies>'
        else:
            self.policyXml = policyXml

    def to_dict(self) -> dict:
        product_dict = {'name': self.name, 'displayName': self.displayName, 'description': self.description, 'state': self.state, 'subscriptionRequired': self.subscriptionRequired, 'approvalRequired': self.approvalRequired}
        if self.policyXml is not None:
            product_dict['policyXml'] = self.policyXml
        return product_dict