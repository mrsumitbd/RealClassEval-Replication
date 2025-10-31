import itertools
import time

class Timer:

    def __init__(self, stmt='pass', setup='pass', teardown='pass', globals=None):
        self.local_ns = {}
        self.global_ns = {} if globals is None else globals
        self.filename = DUMMY_SRC_NAME
        init = ''
        if isinstance(setup, str):
            compile(setup, self.filename, 'exec')
            full = setup + '\n'
            setup = reindent(setup, 4)
        elif callable(setup):
            self.local_ns['_setup'] = setup
            init += ', _setup=_setup'
            full = ''
            setup = '_setup()'
        else:
            raise ValueError('setup is neither a string nor callable')
        if isinstance(stmt, str):
            compile(full + stmt, self.filename, 'exec')
            full = full + stmt + '\n'
            stmt = reindent(stmt, 8)
        elif callable(stmt):
            self.local_ns['_stmt'] = stmt
            init += ', _stmt=_stmt'
            full = ''
            stmt = '_stmt()'
        else:
            raise ValueError('stmt is neither a string nor callable')
        if isinstance(teardown, str):
            compile(full + teardown, self.filename, 'exec')
            teardown = reindent(teardown, 4)
        elif callable(teardown):
            self.local_ns['_teardown'] = teardown
            init += ', _teardown=_teardown'
            teardown = '_teardown()'
        else:
            raise ValueError('teardown is neither a string nor callable')
        if PYPY:
            template = PYPY_TEMPLATE
        else:
            template = TEMPLATE
        src = template.format(stmt=stmt, setup=setup, init=init, teardown=teardown)
        self.src = src

    def make_inner(self):
        code = compile(self.src, self.filename, 'exec')
        global_ns = dict(self.global_ns)
        local_ns = dict(self.local_ns)
        exec(code, global_ns, local_ns)
        return local_ns['inner']

    def update_linecache(self):
        import linecache
        linecache.cache[self.filename] = (len(self.src), None, self.src.split('\n'), self.filename)

    def time_func(self, loops):
        inner = self.make_inner()
        timer = time.perf_counter
        if not PYPY:
            it = itertools.repeat(None, loops)
            return inner(it, timer)
        else:
            return inner(loops, timer)