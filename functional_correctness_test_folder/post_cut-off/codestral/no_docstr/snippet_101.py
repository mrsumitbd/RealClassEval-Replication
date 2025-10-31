
import numpy as np
from scipy.linalg import cholesky


class KalmanFilterXYAH:
    def __init__(self):
        self._motion_mat = np.eye(8)
        for i in range(4):
            self._motion_mat[i, i+4] = 1

        self._update_mat = np.eye(4, 8)

        self._std_weight_position = 1. / 20
        self._std_weight_velocity = 1. / 160

    def initiate(self, measurement: np.ndarray) -> tuple:
        mean_pos = measurement[:4]
        mean_vel = np.zeros_like(mean_pos)
        mean = np.r_[mean_pos, mean_vel]

        std = [
            2 * self._std_weight_position * measurement[3],
            2 * self._std_weight_position * measurement[3],
            1e-2,
            2 * self._std_weight_position * measurement[3],
            10 * self._std_weight_velocity * measurement[3],
            10 * self._std_weight_velocity * measurement[3],
            1e-5,
            10 * self._std_weight_velocity * measurement[3]
        ]
        covariance = np.diag(np.square(std))

        return mean, covariance

    def predict(self, mean: np.ndarray, covariance: np.ndarray) -> tuple:
        std_pos = [
            self._std_weight_position * mean[3],
            self._std_weight_position * mean[3],
            1e-2,
            self._std_weight_position * mean[3]
        ]
        std_vel = [
            self._std_weight_velocity * mean[3],
            self._std_weight_velocity * mean[3],
            1e-5,
            self._std_weight_velocity * mean[3]
        ]

        motion_cov = np.diag(np.square(np.r_[std_pos, std_vel]))

        mean = np.dot(self._motion_mat, mean)
        covariance = np.linalg.multi_dot((
            self._motion_mat, covariance, self._motion_mat.T)) + motion_cov

        return mean, covariance

    def project(self, mean: np.ndarray, covariance: np.ndarray) -> tuple:
        std = [
            self._std_weight_position * mean[3],
            self._std_weight_position * mean[3],
            1e-1,
            self._std_weight_position * mean[3]
        ]
        innovation_cov = np.diag(np.square(std))

        mean = np.dot(self._update_mat, mean)
        covariance = np.linalg.multi_dot((
            self._update_mat, covariance, self._update_mat.T))

        return mean, covariance + innovation_cov

    def multi_predict(self, mean: np.ndarray, covariance: np.ndarray) -> tuple:
        if len(mean.shape) == 1:
            mean = np.expand_dims(mean, axis=0)
        if len(covariance.shape) == 2:
            covariance = np.expand_dims(covariance, axis=0)

        mean = np.dot(mean, self._motion_mat.T)

        std_pos = [
            self._std_weight_position * mean[:, 3],
            self._std_weight_position * mean[:, 3],
            1e-2 * np.ones_like(mean[:, 3]),
            self._std_weight_position * mean[:, 3]
        ]
        std_vel = [
            self._std_weight_velocity * mean[:, 3],
            self._std_weight_velocity * mean[:, 3],
            1e-5 * np.ones_like(mean[:, 3]),
            self._std_weight_velocity * mean[:, 3]
        ]

        motion_cov = np.zeros((mean.shape[0], 8, 8))
        for i in range(4):
            motion_cov[:, i, i] = np.square(std_pos[i])
            motion_cov[:, i+4, i+4] = np.square(std_vel[i])

        covariance = np.matmul(
            np.matmul(self._motion_mat, covariance), self._motion_mat.T) + motion_cov

        return mean, covariance

    def update(self, mean: np.ndarray, covariance: np.ndarray, measurement: np.ndarray) -> tuple:
        projected_mean, projected_cov = self.project(mean, covariance)

        chol_factor, lower = cholesky(
            projected_cov, lower=True, check_finite=False)
        kalman_gain = np.linalg.solve(
            chol_factor.T,
            np.linalg.solve(chol_factor, np.dot(
                covariance, self._update_mat.T).T).T
        ).T

        innovation = measurement - projected_mean

        new_mean = mean + np.dot(innovation, kalman_gain.T)
        new_covariance = covariance - np.linalg.multi_dot((
            kalman_gain, projected_cov, kalman_gain.T))

        return new_mean, new_covariance

    def gating_distance(self, mean: np.ndarray, covariance: np.ndarray, measurements: np.ndarray, only_position: bool = False, metric: str = 'maha') -> np.ndarray:
        mean, covariance = self.project(mean, covariance)
        if only_position:
            mean, covariance = mean[:2], covariance[:2, :2]
            measurements = measurements[:, :2]

        d = measurements.shape[1]
        if metric == 'gaussian':
            return np.sum(np.square(measurements - mean), axis=1)
        elif metric == 'maha':
            cholesky_factor = np.linalg.cholesky(covariance)
            d = measurements - mean
            z = np.linalg.solve(cholesky_factor, d.T).T
            squared_maha = np.sum(np.square(z), axis=1)
            return squared_maha
        else:
            raise ValueError(
                'Invalid metric; must be either "gaussian" or "maha"')
