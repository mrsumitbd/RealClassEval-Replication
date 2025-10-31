from django.contrib.staticfiles.storage import staticfiles_storage
from pipeline.utils import set_std_streams_blocking, to_class
from pipeline.conf import settings
from django.contrib.staticfiles import finders

class Compiler:

    def __init__(self, storage=None, verbose=False):
        if storage is None:
            storage = staticfiles_storage
        self.storage = storage
        self.verbose = verbose

    @property
    def compilers(self):
        return [to_class(compiler) for compiler in settings.COMPILERS]

    def compile(self, paths, compiler_options={}, force=False):

        def _compile(input_path):
            for compiler in self.compilers:
                compiler = compiler(verbose=self.verbose, storage=self.storage)
                if compiler.match_file(input_path):
                    try:
                        infile = self.storage.path(input_path)
                    except NotImplementedError:
                        infile = finders.find(input_path)
                    project_infile = finders.find(input_path)
                    outfile = compiler.output_path(infile, compiler.output_extension)
                    outdated = compiler.is_outdated(project_infile, outfile)
                    compiler.compile_file(project_infile, outfile, outdated=outdated, force=force, **compiler_options)
                    return compiler.output_path(input_path, compiler.output_extension)
            else:
                return input_path
        try:
            import multiprocessing
            from concurrent import futures
        except ImportError:
            return list(map(_compile, paths))
        else:
            with futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
                return list(executor.map(_compile, paths))