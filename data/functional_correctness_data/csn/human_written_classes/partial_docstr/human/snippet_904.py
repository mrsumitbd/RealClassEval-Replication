from abc import ABCMeta, abstractmethod
import numpy as np

class FeatureMatcher:
    """
    Generic feature matching between local features on a source and
    target object using nearest neighbors.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @staticmethod
    def get_point_index(point, all_points, eps=0.0001):
        """Get the index of a point in an array"""
        inds = np.where(np.linalg.norm(point - all_points, axis=1) < eps)
        if inds[0].shape[0] == 0:
            return -1
        return inds[0][0]

    @abstractmethod
    def match(self, source_obj, target_obj):
        """
        Matches features between a source and target object. Source and target
        object types depend on subclass implementation.
        """
        pass