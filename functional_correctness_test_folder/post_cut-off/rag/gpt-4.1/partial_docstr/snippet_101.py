
import numpy as np


class KalmanFilterXYAH:
    '''
    A KalmanFilterXYAH class for tracking bounding boxes in image space using a Kalman filter.
    Implements a simple Kalman filter for tracking bounding boxes in image space. The 8-dimensional state space
    (x, y, a, h, vx, vy, va, vh) contains the bounding box center position (x, y), aspect ratio a, height h, and their
    respective velocities. Object motion follows a constant velocity model, and bounding box location (x, y, a, h) is
    taken as a direct observation of the state space (linear observation model).
    '''

    def __init__(self):
        '''
        Initialize Kalman filter model matrices with motion and observation uncertainty weights.
        The Kalman filter is initialized with an 8-dimensional state space (x, y, a, h, vx, vy, va, vh), where (x, y)
        represents the bounding box center position, 'a' is the aspect ratio, 'h' is the height, and their respective
        velocities are (vx, vy, va, vh). The filter uses a constant velocity model for object motion and a linear
        observation model for bounding box location.
        '''
        ndim, dt = 4, 1.
        self._ndim = ndim
        self._dt = dt
        self._motion_mat = np.eye(2 * ndim, dtype=np.float32)
        for i in range(ndim):
            self._motion_mat[i, ndim + i] = dt
        self._update_mat = np.eye(ndim, 2 * ndim, dtype=np.float32)
        self._std_weight_position = 1. / 20
        self._std_weight_velocity = 1. / 160

    def initiate(self, measurement: np.ndarray) -> tuple:
        '''
        Create a track from an unassociated measurement.
        '''
        mean = np.zeros(8, dtype=np.float32)
        mean[:4] = measurement
        std = [
            2 * self._std_weight_position * measurement[3],  # x
            2 * self._std_weight_position * measurement[3],  # y
            1e-2,                                            # a
            2 * self._std_weight_position * measurement[3],  # h
            10 * self._std_weight_velocity * measurement[3],  # vx
            10 * self._std_weight_velocity * measurement[3],  # vy
            1e-5,                                            # va
            10 * self._std_weight_velocity * measurement[3],  # vh
        ]
        covariance = np.diag(np.square(std)).astype(np.float32)
        return mean, covariance

    def predict(self, mean: np.ndarray, covariance: np.ndarray) -> tuple:
        '''
        Run Kalman filter prediction step.
        '''
        std_pos = self._std_weight_position * mean[3]
        std_vel = self._std_weight_velocity * mean[3]
        motion_cov = np.diag([
            std_pos**2, std_pos**2, 1e-4, std_pos**2,
            std_vel**2, std_vel**2, 1e-6, std_vel**2
        ]).astype(np.float32)
        mean = np.dot(self._motion_mat, mean)
        covariance = np.dot(np.dot(self._motion_mat, covariance),
                            self._motion_mat.T) + motion_cov
        return mean, covariance

    def project(self, mean: np.ndarray, covariance: np.ndarray) -> tuple:
        '''
        Project state distribution to measurement space.
        '''
        std = [
            self._std_weight_position * mean[3],
            self._std_weight_position * mean[3],
            1e-1,
            self._std_weight_position * mean[3]
        ]
        innovation_cov = np.diag(np.square(std)).astype(np.float32)
        mean_proj = np.dot(self._update_mat, mean)
        covariance_proj = np.dot(
            np.dot(self._update_mat, covariance), self._update_mat.T) + innovation_cov
        return mean_proj, covariance_proj

    def multi_predict(self, mean: np.ndarray, covariance: np.ndarray) -> tuple:
        '''
        Run Kalman filter prediction step for multiple object states (Vectorized version).
        '''
        N = mean.shape[0]
        std_pos = self._std_weight_position * mean[:, 3]
        std_vel = self._std_weight_velocity * mean[:, 3]
        motion_cov = np.zeros((N, 8, 8), dtype=np.float32)
        for i in range(N):
            motion_cov[i] = np.diag([
                std_pos[i]**2, std_pos[i]**2, 1e-4, std_pos[i]**2,
                std_vel[i]**2, std_vel[i]**2, 1e-6, std_vel[i]**2
            ])
        mean = np.dot(mean, self._motion_mat.T)
        covariance = np.matmul(
            np.matmul(self._motion_mat, covariance), self._motion_mat.T) + motion_cov
        return mean, covariance

    def update(self, mean: np.ndarray, covariance: np.ndarray, measurement: np.ndarray) -> tuple:
        '''
        Run Kalman filter correction step.
        '''
        projected_mean, projected_cov = self.project(mean, covariance)
        chol_factor = np.linalg.cholesky(projected_cov)
        kalman_gain = np.linalg.solve(
            chol_factor.T, np.linalg.solve(
                chol_factor, np.dot(covariance, self._update_mat.T)).T
        ).T
        innovation = measurement - projected_mean
        new_mean = mean + np.dot(kalman_gain, innovation)
        new_covariance = covariance - \
            np.dot(kalman_gain, np.dot(projected_cov, kalman_gain.T))
        return new_mean, new_covariance

    def gating_distance(self, mean: np.ndarray, covariance: np.ndarray, measurements: np.ndarray, only_position: bool = False, metric: str = 'maha') -> np.ndarray:
        '''
        Compute gating distance between state distribution and measurements.
        '''
        mean_proj, cov_proj = self.project(mean, covariance)
        if only_position:
            mean_proj = mean_proj[:2]
            cov_proj = cov_proj[:2, :2]
            measurements = measurements[:, :2]
        else:
            mean_proj = mean_proj[:4]
            cov_proj = cov_proj[:4, :4]
            measurements = measurements[:, :4]
        d = measurements - mean_proj
        if metric == 'maha':
            cholesky = np.linalg.cholesky(cov_proj)
            z = np.linalg.solve(cholesky, d.T)
            squared_maha = np.sum(z * z, axis=0)
            return squared_maha
        elif metric == 'gaussian':
            squared_euclid = np.sum(d * d, axis=1)
            return squared_euclid
        else:
            raise ValueError("Invalid metric: {}".format(metric))
