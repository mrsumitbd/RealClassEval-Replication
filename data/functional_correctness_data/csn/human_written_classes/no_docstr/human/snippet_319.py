from bambi.backend.terms import CommonTerm, GroupSpecificTerm, HSGPTerm, InterceptTerm, ResponseTerm

class ResponseComponent:

    def __init__(self, component):
        self.component = component

    def build(self, pymc_backend, bmb_model):
        response_term = ResponseTerm(self.component.term, bmb_model.family)
        response_term.build(pymc_backend, bmb_model)