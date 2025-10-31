class OutputFilter:

    def begin_member(self: 'OutputFilter', parent: 'InstanceNode', node: 'InstanceNode', attributes: dict) -> bool:
        return True

    def end_member(self: 'OutputFilter', parent: 'InstanceNode', node: 'InstanceNode', attributes: dict) -> bool:
        return True

    def begin_element(self: 'OutputFilter', parent: 'InstanceNode', node: 'InstanceNode', attributes: dict) -> bool:
        return True

    def end_element(self: 'OutputFilter', parent: 'InstanceNode', node: 'InstanceNode', attributes: dict) -> bool:
        return True