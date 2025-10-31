from opto.trace.nodes import ParameterNode

class TracedFlow:

    def __init__(self, flow):
        object.__setattr__(self, '_flow', flow)
        self.template = ParameterNode(self._flow.template, description='A prompt for Q&A bot with instructions for complete and accurate answers')
        self.dataset_description = ParameterNode(self._flow.dataset_description, description='A description of the dataset with the grounding data')

    def __getattr__(self, name):
        return getattr(self._flow, name)