from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from optuna.trial import FrozenTrial, TrialState
import sklearn.preprocessing
from sklearn.tree import DecisionTreeClassifier
from loguru import logger
from numpy.typing import NDArray
from optuna.distributions import BaseDistribution, CategoricalDistribution
import numpy as np

class DefaultGroupClassifier:
    """
    Create a Decision Tree classifier on the parent group to determine which child group will be sampled.
    """

    def __init__(self) -> None:
        self.classifiers: Dict[int, DecisionTreeClassifier] = {}
        self.encoders: Dict[str, Callable[[NDArray[np.float64]], Union[NDArray[np.float64], NDArray[np.int_]]]] = {}
        self._groups: List[Dict[str, BaseDistribution]] = []

    def __call__(self, samples: Dict[str, NDArray[np.float64]], trials: List[FrozenTrial], groups: List[Dict[str, BaseDistribution]], child_group_indices: List[int], parent_group_index: int) -> NDArray[np.int_]:
        """
        Make predictions based on the sampled parent parameters of which child group will be sampled.
        """
        self._validate_cache(groups)
        parent_group = groups[parent_group_index]
        self._create_encoders(parent_group)
        trial_features = self._create_trial_features(trials, parent_group)
        trial_targets = self._create_trial_targets(trials, child_group_indices)
        self._fit_classifier(trial_features, trial_targets, parent_group_index)
        sample_features = self._create_sample_features(samples, parent_group)
        class_label_predictions = self.classifiers[parent_group_index].predict(sample_features)
        predictions: NDArray[np.int_] = self.classifiers[parent_group_index].classes_[class_label_predictions]
        return predictions

    def _validate_cache(self, groups: List[Dict[str, BaseDistribution]]) -> None:
        """
        Check if.
        """
        if self._groups != groups:
            if len(self._groups) > 0:
                logger.debug(f'groups were {self._groups}, now {groups}')
            self._groups = groups
            self.classifiers = {}

    def _create_encoders(self, group: Dict[str, BaseDistribution]) -> None:
        for param_name, distribution in group.items():
            if param_name in self.encoders:
                continue
            if isinstance(distribution, CategoricalDistribution):
                choices = [distribution.to_internal_repr(choice) for choice in distribution.choices]
                self.encoders[param_name] = lambda x: sklearn.preprocessing.label_binarize(x, classes=choices)
            else:
                self.encoders[param_name] = lambda x: np.asarray(x).reshape(-1, 1)

    def _create_trial_features(self, trials: List[FrozenTrial], group: Dict[str, BaseDistribution]) -> NDArray[np.float64]:
        features = []
        for param_name, distribution in group.items():
            internal_repr: NDArray[np.float64] = np.asarray([distribution.to_internal_repr(trial.params[param_name]) for trial in trials])
            param_features = self.encoders[param_name](internal_repr)
            features.append(param_features)
        features_: NDArray[np.float64] = np.concatenate(features, axis=1)
        assert len(trials) == features_.shape[0]
        return features_

    def _create_trial_targets(self, trials: List[FrozenTrial], group_indices: List[int]) -> NDArray[np.int_]:
        n_groups = len(group_indices)
        targets = []
        for trial in trials:
            trial_params = set(trial.params)
            for target_idx, group_idx in enumerate(group_indices):
                if trial_params.issuperset(self._groups[group_idx]):
                    targets.append(target_idx)
                    break
            else:
                targets.append(n_groups)
        targets_ = np.asarray(targets)
        assert targets_.shape[0] == len(trials)
        return targets_

    def _fit_classifier(self, features: NDArray[np.float64], targets: NDArray[np.int_], index: int) -> None:
        if index in self.classifiers:
            predictions = self.classifiers[index].predict(features)
            if (predictions == targets).all():
                return
        n_samples = features.shape[0]
        for depth in range(1, n_samples):
            classifier = DecisionTreeClassifier(max_depth=depth, max_features=1)
            classifier.fit(features, targets)
            predictions = classifier.predict(features)
            if (predictions == targets).all():
                self.classifiers[index] = classifier
                return
        raise RuntimeError('Could not fit classifier')

    def _create_sample_features(self, samples: Dict[str, NDArray[np.float64]], parent_group: Dict[str, BaseDistribution]) -> NDArray[np.float64]:
        sample_features: List[Union[NDArray[np.float64], NDArray[np.int_]]] = []
        for param_name in parent_group:
            param_features: Union[NDArray[np.float64], NDArray[np.int_]] = self.encoders[param_name](samples[param_name])
            sample_features.append(param_features)
        sample_features_: NDArray[np.float64] = np.concatenate(sample_features, axis=1)
        return sample_features_