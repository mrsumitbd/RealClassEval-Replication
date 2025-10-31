import random

class RandomTask:
    """Special bootcamp that randomly selects from available bootcamps on each call."""

    def __init__(self, **params):
        self.registry = BootcampRegistry()
        self.registry.discover_bootcamps()
        self.available_bootcamps = self.registry.list_available_bootcamps()
        self.available_bootcamps = [name for name in self.available_bootcamps if not any((x in name.lower() for x in ['base', 'template', '{puzzlename}']))]
        self.params = params
        self.current_bootcamp = None
        self.current_bootcamp_name = None
        logger.info(f'RandomTask initialized with {len(self.available_bootcamps)} available bootcamps')

    def case_generator(self) -> object:
        """Generate a case by randomly selecting a bootcamp."""
        self.current_bootcamp_name = random.choice(self.available_bootcamps)
        self.current_bootcamp = self.registry.create_bootcamp_instance(self.current_bootcamp_name, **self.params)
        case = self.current_bootcamp.case_generator()
        if isinstance(case, dict):
            case['_bootcamp_name'] = self.current_bootcamp_name
        else:
            case = {'data': case, '_bootcamp_name': self.current_bootcamp_name}
        return case

    def prompt_func(self, identity) -> str:
        """Generate prompt using the current bootcamp."""
        bootcamp_name = identity.get('_bootcamp_name', self.current_bootcamp_name)
        if not self.current_bootcamp or self.current_bootcamp_name != bootcamp_name:
            self.current_bootcamp_name = bootcamp_name
            self.current_bootcamp = self.registry.create_bootcamp_instance(bootcamp_name, **self.params)
        identity_copy = dict(identity)
        identity_copy.pop('_bootcamp_name', None)
        if 'data' in identity_copy and len(identity_copy) == 1:
            identity_copy = identity_copy['data']
        return self.current_bootcamp.prompt_func(identity_copy)

    @classmethod
    def extract_output(cls, output):
        """This should not be called directly for RandomTask."""
        raise NotImplementedError('RandomTask does not implement extract_output directly')

    @classmethod
    def _verify_correction(cls, solution, identity):
        """This should not be called directly for RandomTask."""
        raise NotImplementedError('RandomTask does not implement _verify_correction directly')

    def verify_score(self, model_output, identity, format_score=0, short_penalty=True, short_threshold=100, format_penalty=True) -> float:
        """Verify score using the appropriate bootcamp."""
        bootcamp_name = identity.get('_bootcamp_name', self.current_bootcamp_name)
        if not self.current_bootcamp or self.current_bootcamp_name != bootcamp_name:
            self.current_bootcamp_name = bootcamp_name
            self.current_bootcamp = self.registry.create_bootcamp_instance(bootcamp_name, **self.params)
        identity_copy = dict(identity)
        identity_copy.pop('_bootcamp_name', None)
        if 'data' in identity_copy and len(identity_copy) == 1:
            identity_copy = identity_copy['data']
        return self.current_bootcamp.verify_score(model_output, identity_copy, format_score, short_penalty, short_threshold, format_penalty)