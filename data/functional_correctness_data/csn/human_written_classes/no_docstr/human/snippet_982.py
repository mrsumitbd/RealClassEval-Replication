import ef_conf_utils

class Context:

    def __init__(self, profile, region, env, service, template_path, no_params, verbose, lint, silent, skip_symbols):
        self.profile = profile
        self.region = region
        self.env = env
        self.service = service
        self.template_path = template_path
        self.no_params = no_params
        self.param_path = ef_conf_utils.get_template_parameters_file(self.template_path)
        self.verbose = verbose
        self.lint = lint
        self.silent = silent
        self.skip_symbols = skip_symbols

    def __str__(self):
        return 'profile: {}\nregion: {}\nenv: {}\nservice: {}\ntemplate_path: {}\nparam_path: {}\nlint: {}'.format(self.profile, self.region, self.env, self.service, self.template_path, self.param_path, self.lint)