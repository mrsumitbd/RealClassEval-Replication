from ford.sourceform import ExternalBoundProcedure, ExternalFunction, ExternalInterface, ExternalModule, ExternalProgram, ExternalSourceFile, ExternalSubmodule, ExternalSubroutine, ExternalType, FortranBlockData, FortranContainer, FortranInterface, FortranModule, FortranModuleProcedureInterface, FortranProcedure, FortranProgram, FortranSourceFile, FortranSubmodule, FortranModuleProcedureImplementation, FortranBoundProcedure, FortranType
from ford.utils import traverse, ProgressBar
import pathlib
from tqdm.contrib.concurrent import process_map
import os
from typing import Dict, Iterable, List, Optional, Set, Tuple, Type, Union, cast

class GraphManager:
    """Collection of graphs of the various relationships between a set
    of entities

    Contains graphs of module use relations, type relations, call
    trees, etc. It manages these, ensures that everything that is
    needed is added at the correct time, and produces the plots for
    the list pages.

    Parameters
    ----------
    graphdir:
        The location of the graphs within the output tree.
    parentdir:
        Location of top-level directory
    coloured_edges:
        If true, arrows in graphs use different colours to help
        distinguish them
    show_proc_parent:
        If true, show the parent of a procedure in the call graph
        as part of the label
    save_graphs:
        If true, save graphs as separate files, as well as embedding
        them in the HTML
    """

    def __init__(self, graphdir: os.PathLike, parentdir: str, coloured_edges: bool, show_proc_parent: bool, save_graphs: bool=False):
        self.graph_objs: List[FortranContainer] = []
        self.modules: Set[FortranContainer] = set()
        self.programs: Set[FortranContainer] = set()
        self.procedures: Set[FortranContainer] = set()
        self.internal_procedures: Set[FortranContainer] = set()
        self.bound_procedures: Set[FortranContainer] = set()
        self.types: Set[FortranContainer] = set()
        self.sourcefiles: Set[FortranContainer] = set()
        self.blockdata: Set[FortranContainer] = set()
        self.save_graphs = save_graphs
        self.graphdir = pathlib.Path(graphdir)
        self.usegraph = None
        self.typegraph = None
        self.callgraph = None
        self.filegraph = None
        self.data = GraphData(parentdir, coloured_edges, show_proc_parent)

    def register(self, obj: FortranContainer):
        """Register ``obj`` as a node to be used in graphs"""
        if obj.meta.graph:
            self.data.register(obj)
            self.graph_objs.append(obj)

    def graph_all(self):
        """Create all graphs"""
        for obj in (bar := ProgressBar('Generating graphs', sorted(self.graph_objs))):
            bar.set_current(obj.name)
            if is_module(obj):
                obj.usesgraph = UsesGraph(obj, self.data)
                obj.usedbygraph = UsedByGraph(obj, self.data)
                self.modules.add(obj)
            elif is_type(obj):
                obj.inhergraph = InheritsGraph(obj, self.data)
                obj.inherbygraph = InheritedByGraph(obj, self.data)
                self.types.add(obj)
                for bp in getattr(obj, 'boundprocs', []):
                    if not (len(bp.bindings) == 1 and (not isinstance(bp.bindings[0], FortranBoundProcedure))):
                        self.bound_procedures.add(bp)
            elif is_proc(obj):
                obj.callsgraph = CallsGraph(obj, self.data)
                obj.calledbygraph = CalledByGraph(obj, self.data)
                obj.usesgraph = UsesGraph(obj, self.data)
                self.procedures.add(obj)
                for p in traverse(obj, ['subroutines', 'functions']):
                    self.internal_procedures.add(p) if getattr(p, 'visible', False) else None
            elif is_program(obj):
                obj.usesgraph = UsesGraph(obj, self.data)
                obj.callsgraph = CallsGraph(obj, self.data)
                self.programs.add(obj)
            elif is_sourcefile(obj):
                obj.afferentgraph = AfferentGraph(obj, self.data)
                obj.efferentgraph = EfferentGraph(obj, self.data)
                self.sourcefiles.add(obj)
            elif is_blockdata(obj):
                obj.usesgraph = UsesGraph(obj, self.data)
                self.blockdata.add(obj)
        usenodes = sorted(list(self.modules))
        callnodes = sorted(list(self.procedures | self.internal_procedures | self.bound_procedures))
        for p in sorted(self.programs):
            if len(p.usesgraph.added) > 1:
                usenodes.append(p)
            if len(p.callsgraph.added) > 1:
                callnodes.append(p)
        for p in sorted(self.procedures):
            if len(p.usesgraph.added) > 1:
                usenodes.append(p)
        for b in self.blockdata:
            if len(b.usesgraph.added) > 1:
                usenodes.append(b)
        self.usegraph = ModuleGraph(usenodes, self.data, 'module~~graph')
        self.typegraph = TypeGraph(self.types, self.data, 'type~~graph')
        self.callgraph = CallGraph(callnodes, self.data, 'call~~graph')
        self.filegraph = FileGraph(self.sourcefiles, self.data, 'file~~graph')

    def output_graphs(self, njobs=0):
        """Save graphs to file"""
        if not self.save_graphs:
            return
        self.graphdir.mkdir(exist_ok=True, parents=True, mode=493)
        if njobs == 0:
            for m in self.modules:
                m.usesgraph.create_svg(self.graphdir)
                m.usedbygraph.create_svg(self.graphdir)
            for t in self.types:
                t.inhergraph.create_svg(self.graphdir)
                t.inherbygraph.create_svg(self.graphdir)
            for p in self.procedures:
                p.callsgraph.create_svg(self.graphdir)
                p.calledbygraph.create_svg(self.graphdir)
            for p in self.programs:
                p.callsgraph.create_svg(self.graphdir)
                p.usesgraph.create_svg(self.graphdir)
            for f in self.sourcefiles:
                f.afferentgraph.create_svg(self.graphdir)
                f.efferentgraph.create_svg(self.graphdir)
            for b in self.blockdata:
                b.usesgraph.create_svg(self.graphdir)
        else:
            args = []
            args.extend([(m.usesgraph, m.usedbygraph, self.graphdir) for m in self.modules])
            args.extend([(m.inhergraph, m.inherbygraph, self.graphdir) for m in self.types])
            args.extend([(m.callsgraph, m.calledbygraph, self.graphdir) for m in self.procedures])
            args.extend([(m.callsgraph, m.usesgraph, self.graphdir) for m in self.programs])
            args.extend([(m.afferentgraph, m.efferentgraph, self.graphdir) for m in self.sourcefiles])
            args.extend([(m.usesgraph, self.graphdir) for m in self.blockdata])
            process_map(outputFuncWrap, args, max_workers=njobs, desc='Writing graphs', chunksize=1)
        for graph in [self.usegraph, self.typegraph, self.callgraph, self.filegraph]:
            if graph:
                graph.create_svg(self.graphdir)