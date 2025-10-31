class StoryLoopAPI:
    """
    loop (scope) concept similar to switch (forking)
    the main difference is that after case switch jump to the next part
    after last case. But in scope it loop until
    - we get receive unmatched message
    - or break loop explicitly
    """

    def __init__(self, library, parser_instance):
        self.library = library
        self.parser_instance = parser_instance

    def loop(self):

        def fn(one_loop):
            scope_node = StoriesLoopNode(one_loop)
            self.parser_instance.add_to_current_node(scope_node)
            self.parser_instance.compile_scope(scope_node, one_loop)
            return one_loop
        return fn