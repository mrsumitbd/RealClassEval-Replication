class Heuristics:
    EVENTS = {'before_request', 'after_headers', 'after_response', 'on_timeout', 'on_request_successful', 'on_host_unreachable'}

    def __init__(self, kb=None, request_engine=None):
        self.rulesets = {event: RuleSet() for event in self.EVENTS}
        self.kb = kb
        self.request_engine = request_engine
        for key, rs in self.rulesets.items():
            setattr(self, key, rs.accept)

    def add_multiple(self, iterator):
        for h in iterator:
            self.add(h)

    def add(self, heuristic):
        applied = False
        supported = dir(heuristic)
        if 'set_engine' in supported and self.request_engine is not None:
            heuristic.set_engine(self.request_engine)
        if 'set_kb' in supported and self.kb is not None:
            try:
                heuristic.set_kb(self.kb)
            except AttributeError:
                if 'load_kb' in supported:
                    heuristic.load_kb(self.kb)
                else:
                    raise
        if 'set_child_heuristics' in supported:
            heuristic.set_child_heuristics(Heuristics(request_engine=self.request_engine, kb=self.kb))
        for event in self.EVENTS:
            if event in supported:
                self.rulesets[event].add(getattr(heuristic, event))
                applied = True
        if not applied:
            raise ValueError('Expecting heuristic to support some of %s' % self.EVENTS)