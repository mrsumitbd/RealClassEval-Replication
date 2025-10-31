import numpy as np

class Link:
    """
    Base Link class.

    Parameters
    ----------
    name: string
        The name of the link
    bounds: tuple
        Optional : The bounds of the link. Defaults to None

    Attributes
    ----------
    has_rotation: bool
        Whether the link provides a rotation
    length: float
        Length of the link
    """

    def __init__(self, name, length, bounds=None, is_final=False):
        if bounds is None:
            self.bounds = (-np.inf, np.inf)
        else:
            self.bounds = bounds
        self.name = name
        self.length = length
        self.axis_length = length
        self.is_final = is_final
        self.has_rotation = False
        self.has_translation = False
        self.joint_type = None

    def __repr__(self):
        return 'Link name={} bounds={}'.format(self.name, self.bounds)

    def get_rotation_axis(self):
        """

        Returns
        -------
        coords:
            coordinates of the rotation axis in the frame of the joint

        """
        raise ValueError("This Link doesn't have a rotation axis")

    def get_link_frame_matrix(self, actuator_parameters: dict):
        """
        Return the frame matrix corresponding to the link, parameterized with theta

        Parameters
        ----------
        actuator_parameters: dict
            Values for the actuator movements

        Note
        ----
        Theta works for rotations, and for other one-dimensional actuators (ex: prismatic joints), even if the name can be misleading
        """
        raise NotImplementedError