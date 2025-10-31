class CallableStoriesAPI:

    def __init__(self, library, parser_instance, processor_instance):
        self.library = library
        self.parser_instance = parser_instance
        self.processor_instance = processor_instance

    def callable(self):

        def fn(callable_story):
            compiled_story = self.parser_instance.compile(callable_story)
            self.library.add_callable(compiled_story)
            return CallableNodeWrapper(compiled_story, self.library, self.processor_instance).startpoint
        return fn