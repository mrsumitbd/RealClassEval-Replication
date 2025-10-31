
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
        self._ndim = 4
        self._dim_x = 8
        self._dim_z = 4
        self._std_weight_position = 1. / 20
        self._std_weight_velocity = 1. / 160

        # Motion matrix (F)
        self._motion_mat = np.eye(self._dim_x, dtype=np.float32)
        for i in range(self._ndim):
            self._motion_mat[i, self._ndim + i] = 1.

        # Observation matrix (H)
        self._update_mat = np.eye(self._dim_z, self._dim_x, dtype=np.float32)

    def initiate(self, measurement: np.ndarray) -> tuple:
        mean = np.zeros(self._dim_x, dtype=np.float32)
        mean[:self._ndim] = measurement

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
        means = mean.copy()
        covariances = covariance.copy()
        for i in range(means.shape[0]):
            std_pos = self._std_weight_position * means[i, 3]
            std_vel = self._std_weight_velocity * means[i, 3]
            motion_cov = np.diag([
                std_pos**2, std_pos**2, 1e-4, std_pos**2,
                std_vel**2, std_vel**2, 1e-6, std_vel**2
            ]).astype(np.float32)
            means[i] = np.dot(self._motion_mat, means[i])
            covariances[i] = np.dot(
                np.dot(self._motion_mat, covariances[i]), self._motion_mat.T) + motion_cov
        return means, covariances

    def update(self, mean: np.ndarray, covariance: np.ndarray, measurement: np.ndarray) -> tuple:
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
