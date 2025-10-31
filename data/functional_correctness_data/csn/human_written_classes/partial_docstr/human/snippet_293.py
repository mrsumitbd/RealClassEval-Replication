import numpy

class WrappedBooster:

    def __init__(self, booster):
        self.booster_ = booster
        self.n_features_ = self.booster_.feature_name()
        self.objective_ = self.get_objective()
        if self.objective_.startswith('binary'):
            self.operator_name = 'LgbmClassifier'
            self.classes_ = self._generate_classes(booster)
        elif self.objective_.startswith('multiclass'):
            self.operator_name = 'LgbmClassifier'
            self.classes_ = self._generate_classes(booster)
        elif self.objective_.startswith(('regression', 'poisson', 'gamma', 'quantile', 'huber', 'tweedie')):
            self.operator_name = 'LgbmRegressor'
        else:
            raise NotImplementedError('Unsupported LightGbm objective: %r.' % self.objective_)
        try:
            average_output = self.booster_.attr('average_output')
        except AttributeError:
            average_output = self.booster_.params.get('average_output', None)
        if average_output:
            self.boosting_type = 'rf'
        else:
            self.boosting_type = 'gbdt'

    @staticmethod
    def _generate_classes(booster):
        if isinstance(booster, dict):
            num_class = booster['num_class']
        else:
            try:
                num_class = booster.attr('num_class')
            except AttributeError:
                num_class = booster.params.get('num_class', None)
        if num_class is None:
            dp = booster.dump_model(num_iteration=1)
            num_class = dp['num_class']
        if num_class == 1:
            return numpy.asarray([0, 1])
        return numpy.arange(num_class)

    def get_objective(self):
        """Returns the objective."""
        if hasattr(self, 'objective_') and self.objective_ is not None:
            return self.objective_
        try:
            objective = self.booster_.attr('objective')
        except AttributeError:
            objective = self.booster_.params.get('objective', None)
        if objective is not None:
            return objective
        dp = self.booster_.dump_model(num_iteration=1)
        return dp['objective']