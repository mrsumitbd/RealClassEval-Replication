import os

class TuneResults:
    """ Object to represent the tuning results stored to file """

    def __init__(self, results_filename):
        if not os.path.isfile(results_filename):
            raise ValueError('Error: results_filename does not exist')
        meta, data = _read_results_file(results_filename)
        if len(data) < 1:
            raise ValueError('results file seems to be empty or did not load correctly')
        self.data = data
        self.meta = meta
        self.objective = meta['objective']
        self.objective_higher_is_better = meta.get('objective_higher_is_better', False)

    def get_best_config(self, gpu_name='default', problem_size=None):
        """ get the best config based on these tuning results

            This function returns the overall best performing kernel configuration
            based on the tuning results for a given gpu_name and problem_size.

            If problem_size is not given this function will select a default configuration
            based on the tuning results for all problem_sizes and the given gpu_name.

            If gpu_name is not given this function will select a default configuration
            based on all tuning results.

            :param gpu_name: Name of the GPU for which the best configuration
                needs to be retrieved.
            :type gpu_name: string

            :param problem_size: The problem size for which the best configuration
                on the given gpu_name needs to be retrieved.
            :type problem_size: tuple, int, or string

            :returns: A dictionary with tunable parameters of the selected kernel
                kernel configuration.
            :rtype: dict
        """
        gpu_name = gpu_name.replace('-', '_').replace(' ', '_')
        if problem_size:
            if not isinstance(problem_size, str):
                if not isinstance(problem_size, (list, tuple)):
                    problem_size = (problem_size,)
                problem_size_str = 'x'.join((str(i) for i in problem_size))
            else:
                problem_size_str = problem_size
        gpu_match = [result for result in self.data if result['device_name'] == gpu_name]
        if gpu_match:
            gpu_ps_match = [result for result in gpu_match if problem_size and result['problem_size'] == problem_size_str]
            if gpu_ps_match:
                return _get_best_config_from_list(gpu_ps_match, self.objective, self.objective_higher_is_better)
            return _select_best_common_config(gpu_match, self.objective, self.objective_higher_is_better)
        return _select_best_common_config(self.data, self.objective, self.objective_higher_is_better)