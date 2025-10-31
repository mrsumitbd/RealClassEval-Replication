import json

class Recipe:

    def __init__(self):
        self.pipeline_str = None
        '\n        str: The raw pipeline string, with no attribute or directives, except\n        for number indicators for when there are duplicate components.\n        \n        e.g.: "fastqc trimmomatic spades"\n        e.g.: "fastqc trimmomatic (spades#1 | spades#2)\n        '
        self.directives = {}
        '\n        dict: Dictionary with the parameters and directives for each component\n        in the pipeline_str attribute. Missing components will be left with\n        the default parameters and directives. \n        '

    def brew(self):
        if not hasattr(self, 'name'):
            raise eh.RecipeError("Recipe class '{}' does not have a 'name' attribute set".format(self.__class__))
        if not self.pipeline_str:
            raise eh.RecipeError("Recipe with name '{}' does not have a pipeline_str attribute set".format(self.name))
        for component, vals in self.directives.items():
            params = vals.get('params', None)
            directives = vals.get('directives', None)
            if '#' in component:
                _component = component.split('#')[0]
            else:
                _component = component
            component_str = self._get_component_str(_component, params, directives)
            self.pipeline_str = self.pipeline_str.replace(component, component_str)
        return self.pipeline_str

    @staticmethod
    def _get_component_str(component, params=None, directives=None):
        """ Generates a component string based on the provided parameters and
        directives

        Parameters
        ----------
        component : str
            Component name
        params : dict
            Dictionary with parameter information
        directives : dict
            Dictionary with directives information

        Returns
        -------
        str
            Component string with the parameters and directives, ready for
            parsing by flowcraft engine
        """
        final_directives = {}
        if directives:
            final_directives = directives
        if params:
            final_directives['params'] = params
        if final_directives:
            return '{}={}'.format(component, json.dumps(final_directives, separators=(',', ':')))
        else:
            return component