from trinity.utils.log import get_logger

class _BundleAllocator:
    """An allocator for bundles."""

    def __init__(self, node_bundle_map: dict[str, list]) -> None:
        self.logger = get_logger(__name__, in_ray_actor=True)
        self.node_bundle_list = [value for value in node_bundle_map.values()]
        self.node_list = [key for key in node_bundle_map.keys()]
        self.nid = 0
        self.bid = 0

    def allocate(self, num: int) -> list:
        if self.bid + num > len(self.node_bundle_list[self.nid]):
            raise ValueError('Bundle allocation error, a tensor parallel group is allocated across multiple nodes.')
        bundle_list = self.node_bundle_list[self.nid][self.bid:self.bid + num]
        self.logger.info(f'Allocate bundles {bundle_list} on node {self.node_list[self.nid]}.')
        self.bid += num
        if self.bid == len(self.node_bundle_list[self.nid]):
            self.bid = 0
            self.nid += 1
        return bundle_list