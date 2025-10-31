from ford.settings import ProjectSettings, EntitySettings
from ford.graphs import graphviz_installed, GraphManager
from itertools import chain
from dataclasses import asdict
import pathlib
import ford.tipue_search
import os
import shutil
import jinja2
from typing import List, Union, Callable, Type, Tuple
from ford.utils import ProgressBar
import traceback
import time
import sys
from ford.console import warn

class Documentation:
    """
    Represents and handles the creation of the documentation files from
    a project.
    """

    def __init__(self, settings: ProjectSettings, proj_docs: str, project, pagetree):
        env.globals['projectData'] = asdict(settings)
        env.loader = jinja2.FileSystemLoader(settings.html_template_dir + [loc / 'templates'])
        self.project = project
        self.settings = settings
        self.data = {k: v for k, v in asdict(settings).items() if v is not None}
        self.data['pages'] = pagetree
        del self.data['project_url']
        self.lists: List[ListPage] = []
        self.docs = []
        self.njobs = settings.parallel
        self.parallel = self.njobs > 0
        self.index = IndexPage(self.data, project, proj_docs)
        self.search = SearchPage(self.data, project)
        if not graphviz_installed and settings.graph:
            warn('Will not be able to generate graphs. Graphviz not installed.')
        if settings.relative:
            graphparent = '../'
        else:
            graphparent = ''
        print('  Creating HTML documentation... ', end='')
        html_time_start = time.time()
        try:
            PageFactory = Union[Type, Callable]
            entity_list_page_map: List[Tuple[List, PageFactory]] = [(project.types, TypePage), (project.absinterfaces, AbsIntPage), (project.procedures, ProcPage), (project.submodprocedures, ProcPage), (project.modules, ModulePage), (project.submodules, ModulePage), (project.programs, ProgPage), (project.blockdata, BlockPage), (project.namelists, NamelistPage)]
            if settings.incl_src:
                entity_list_page_map.append((project.allfiles, FilePage))
            for entity_list, page_class in entity_list_page_map:
                for item in entity_list:
                    self.docs.append(page_class(self.data, project, item))
            if len(project.procedures) > 0:
                self.lists.append(ProcList(self.data, project))
            if settings.incl_src and len(project.files) + len(project.extra_files) > 1:
                self.lists.append(FileList(self.data, project))
            if len(project.modules) + len(project.submodules) > 0:
                self.lists.append(ModList(self.data, project))
            if len(project.programs) > 1:
                self.lists.append(ProgList(self.data, project))
            if len(project.types) > 0:
                self.lists.append(TypeList(self.data, project))
            if len(project.absinterfaces) > 0:
                self.lists.append(AbsIntList(self.data, project))
            if len(project.blockdata) > 1:
                self.lists.append(BlockList(self.data, project))
            if project.namelists:
                self.lists.append(NamelistList(self.data, project))
            self.pagetree = [PagetreePage(self.data, project, item) for item in pagetree or []]
        except Exception:
            if settings.dbg:
                traceback.print_exc()
                sys.exit('Error encountered.')
            else:
                sys.exit('Error encountered. Run with "--debug" flag for traceback.')
        html_time_end = time.time()
        print(f'done in {html_time_end - html_time_start:5.3f}s')
        self.graphs = GraphManager(self.data.get('graph_dir', ''), graphparent, settings.coloured_edges, settings.show_proc_parent, save_graphs=bool(self.data.get('graph_dir', False)))
        if graphviz_installed and settings.graph:
            for entity_list in [project.types, project.procedures, project.submodprocedures, project.modules, project.submodules, project.programs, project.files, project.blockdata]:
                for item in entity_list:
                    self.graphs.register(item)
            self.graphs.graph_all()
            project.callgraph = self.graphs.callgraph
            project.typegraph = self.graphs.typegraph
            project.usegraph = self.graphs.usegraph
            project.filegraph = self.graphs.filegraph
        else:
            project.callgraph = ''
            project.typegraph = ''
            project.usegraph = ''
            project.filegraph = ''
        if settings.search:
            url = '' if settings.relative else settings.project_url
            self.tipue = ford.tipue_search.Tipue_Search_JSON_Generator(settings.output_dir, url)
            self.tipue.create_node(self.index.html, 'index.html', EntitySettings(category='home'))
            jobs = len(self.docs) + len(self.pagetree)
            for page in (bar := ProgressBar('Creating search index', chain(self.docs, self.pagetree), total=jobs)):
                bar.set_current(page.loc)
                self.tipue.create_node(page.html, page.loc, page.meta)

    def writeout(self) -> None:
        out_dir: pathlib.Path = self.data['output_dir']
        if out_dir.is_file():
            out_dir.unlink()
        else:
            shutil.rmtree(out_dir, ignore_errors=True)
        try:
            out_dir.mkdir(USER_WRITABLE_ONLY, parents=True)
        except Exception as e:
            print(f'Error: Could not create output directory. {e.args[0]}')
        for directory in ['lists', 'sourcefile', 'type', 'proc', 'interface', 'module', 'program', 'src', 'blockdata', 'namelist']:
            (out_dir / directory).mkdir(USER_WRITABLE_ONLY)
        for directory in ['css', 'js', 'webfonts']:
            copytree(loc / directory, out_dir / directory)
        if self.data['graph']:
            self.graphs.output_graphs(self.njobs)
        if self.data['search']:
            copytree(loc / 'search', out_dir / 'search')
            self.tipue.print_output()
        try:
            copytree(self.data['media_dir'], out_dir / 'media')
        except OSError as e:
            warn(f"error copying media directory {self.data['media_dir']}, {e}")
        except KeyError:
            pass
        if 'css' in self.data:
            shutil.copy(self.data['css'], out_dir / 'css' / 'user.css')
        shutil.copy(self.data['favicon'], out_dir / 'favicon.png')
        if self.data['incl_src']:
            for src in self.project.allfiles:
                shutil.copy(src.path, out_dir / 'src' / src.name)
        if 'mathjax_config' in self.data:
            mathjax_path = out_dir / 'js' / 'MathJax-config'
            mathjax_path.mkdir(parents=True, exist_ok=True)
            shutil.copy(self.data['mathjax_config'], mathjax_path / os.path.basename(self.data['mathjax_config']))
        items = list(chain(self.docs, self.lists, self.pagetree, [self.index, self.search]))
        for page in (bar := ProgressBar('Writing files', items)):
            bar.set_current(os.path.relpath(page.outfile))
            page.writeout()
        print(f'\nBrowse the generated documentation: file://{out_dir}/index.html')