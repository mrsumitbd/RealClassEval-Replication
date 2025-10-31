from pipask._vendor.pip._internal.req.req_set import RequirementSet
from pipask._vendor.pip._internal.req.req_install import InstallRequirement
from typing import Callable, List, Optional

class BaseResolver:

    def resolve(self, root_reqs: List[InstallRequirement], check_supported_wheels: bool) -> RequirementSet:
        raise NotImplementedError()

    def get_installation_order(self, req_set: RequirementSet) -> List[InstallRequirement]:
        raise NotImplementedError()