class SoarPlatformInfo:
    """SOAR platform information for a case."""

    def __init__(self, case_id: str, platform_type: str):
        self.case_id = case_id
        self.platform_type = platform_type

    @classmethod
    def from_dict(cls, data: dict) -> 'SoarPlatformInfo':
        """Create from API response dict."""
        return cls(case_id=data.get('caseId'), platform_type=data.get('responsePlatformType'))