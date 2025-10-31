class CallableDynamicDoc:

    def __init__(self, func, doc_tmpl):
        self.__doc_tmpl__ = doc_tmpl
        self.__func__ = func

    def __call__(self, *args, **kwds):
        return self.__func__(*args, **kwds)

    @property
    def __doc__(self):
        opts_desc = _describe_option('all', _print_desc=False)
        opts_list = pp_options_list(list(_registered_options.keys()))
        return self.__doc_tmpl__.format(opts_desc=opts_desc, opts_list=opts_list)