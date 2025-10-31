from collections import OrderedDict
from ipyrad.assemble.utils import IPyradError

class TreeParser:

    def __init__(self, newick, constraint_dict, constraint_exact):
        """Traverses tree to build test sets given constraint options."""
        self.testset = set()
        self.hold = [0, 0, 0, 0]
        self.tree = toytree.tree(newick)
        if not self.tree.is_rooted():
            raise IPyradError('generate_tests_from_tree(): tree must be rooted and resolved')
        self.cdict = OrderedDict(((i, []) for i in ['p1', 'p2', 'p3', 'p4']))
        if constraint_dict:
            self.cdict.update(constraint_dict)
        self.xdict = constraint_exact
        if isinstance(self.xdict, bool):
            self.xdict = [self.xdict] * 4
        if isinstance(self.xdict, list):
            if len(self.xdict) != len(self.cdict):
                raise Exception('constraint_exact must be bool or list of bools length N')
        self.loop()

    def loop(self, node, idx):
        """getting closer...."""
        for topnode in node.traverse():
            for oparent in topnode.children:
                for onode in oparent.traverse():
                    if self.test_constraint(onode, 3):
                        self.hold[3] = onode.idx
                        node2 = oparent.get_sisters()[0]
                        for topnode2 in node2.traverse():
                            for oparent2 in topnode2.children:
                                for onode2 in oparent2.traverse():
                                    if self.test_constraint(onode2, 2):
                                        self.hold[2] = onode2.idx
                                        node3 = oparent2.get_sisters()[0]
                                        for topnode3 in node3.traverse():
                                            for oparent3 in topnode3.children:
                                                for onode3 in oparent3.traverse():
                                                    if self.test_constraint(onode3, 1):
                                                        self.hold[1] = onode3.idx
                                                        node4 = oparent3.get_sisters()[0]
                                                        for topnode4 in node4.traverse():
                                                            for oparent4 in topnode4.children:
                                                                for onode4 in oparent4.traverse():
                                                                    if self.test_constraint(onode4, 0):
                                                                        self.hold[0] = onode4.idx
                                                                        self.testset.add(tuple(self.hold))

    def test_constraint(self, node, idx):
        names = set(node.get_leaf_names())
        const = set(list(self.cdict.values())[idx])
        if const:
            if self.xdict[idx]:
                if names == const:
                    return 1
                else:
                    return 0
            elif len(names.intersection(const)) == len(names):
                return 1
            else:
                return 0
        return 1