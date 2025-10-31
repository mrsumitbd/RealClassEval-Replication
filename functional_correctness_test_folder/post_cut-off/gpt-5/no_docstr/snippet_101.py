import numpy as np


class KalmanFilterXYAH:
    '''
    A KalmanFilterXYAH class for tracking bounding boxes in image space using a Kalman filter.
    Implements a simple Kalman filter for tracking bounding boxes in image space. The 8-dimensional state space
    (x, y, a, h, vx, vy, va, vh) contains the bounding box center position (x, y), aspect ratio a, height h, and their
    respective velocities. Object motion follows a constant velocity model, and bounding box location (x, y, a, h) is
    taken as a direct observation of the state space (linear observation model).
    Attributes:
        _motion_mat (np.ndarray): The motion matrix for the Kalman filter.
        _update_mat (np.ndarray): The update matrix for the Kalman filter.
        _std_weight_position (float): Standard deviation weight for position.
        _std_weight_velocity (float): Standard deviation weight for velocity.
    Methods:
        initiate: Creates a track from an unassociated measurement.
        predict: Runs the Kalman filter prediction step.
        project: Projects the state distribution to measurement space.
        multi_predict: Runs the Kalman filter prediction step (vectorized version).
        update: Runs the Kalman filter correction step.
        gating_distance: Computes the gating distance between state distribution and measurements.
    Examples:
        Initialize the Kalman filter and create a track from a measurement
        >>> kf = KalmanFilterXYAH()
        >>> measurement = np.array([100, 200, 1.5, 50])
        >>> mean, covariance = kf.initiate(measurement)
        >>> print(mean)
        >>> print(covariance)
    '''

    def __init__(self):
        '''
        Initialize Kalman filter model matrices with motion and observation uncertainty weights.
        The Kalman filter is initialized with an 8-dimensional state space (x, y, a, h, vx, vy, va, vh), where (x, y)
        represents the bounding box center position, 'a' is the aspect ratio, 'h' is the height, and their respective
        velocities are (vx, vy, va, vh). The filter uses a constant velocity model for object motion and a linear
        observation model for bounding box location.
        Examples:
            Initialize a Kalman filter for tracking:
            >>> kf = KalmanFilterXYAH()
        '''
        ndim, dt = 4, 1.0
        self._std_weight_position = 1.0 / 20.0
        self._std_weight_velocity = 1.0 / 160.0

        self._motion_mat = np.eye(2 * ndim, dtype=np.float32)
        for i in range(ndim):
            self._motion_mat[i, ndim + i] = dt

        self._update_mat = np.eye(ndim, 2 * ndim, dtype=np.float32)

    def initiate(self, measurement: np.ndarray) -> tuple:
        '''
        Create a track from an unassociated measurement.
        Args:
            measurement (ndarray): Bounding box coordinates (x, y, a, h) with center position (x, y), aspect ratio a,
                and height h.
        Returns:
            (tuple[ndarray, ndarray]): Returns the mean vector (8-dimensional) and covariance matrix (8x8 dimensional)
                of the new track. Unobserved velocities are initialized to 0 mean.
        Examples:
            >>> kf = KalmanFilterXYAH()
            >>> measurement = np.array([100, 50, 1.5, 200])
            >>> mean, covariance = kf.initiate(measurement)
        '''
        mean = np.zeros(8, dtype=np.float32)
        mean[:4] = measurement.astype(np.float32)

        h = float(measurement[3])
        pos_var = (2.0 * self._std_weight_position * h) ** 2
        vel_var = (10.0 * self._std_weight_velocity * h) ** 2

        cov = np.zeros((8, 8), dtype=np.float32)
        cov[0, 0] = pos_var
        cov[1, 1] = pos_var
        cov[2, 2] = 1e-2  # aspect ratio uncertainty
        cov[3, 3] = pos_var
        cov[4, 4] = vel_var
        cov[5, 5] = vel_var
        cov[6, 6] = 1e-5  # aspect ratio velocity uncertainty
        cov[7, 7] = vel_var

        return mean, cov

    def predict(self, mean: np.ndarray, covariance: np.ndarray) -> tuple:
        '''
        Run Kalman filter prediction step.
        Args:
            mean (ndarray): The 8-dimensional mean vector of the object state at the previous time step.
            covariance (ndarray): The 8x8-dimensional covariance matrix of the object state at the previous time step.
        Returns:
            (tuple[ndarray, ndarray]): Returns the mean vector and covariance matrix of the predicted state. Unobserved
                velocities are initialized to 0 mean.
        Examples:
            >>> kf = KalmanFilterXYAH()
            >>> mean = np.array([0, 0, 1, 1, 0, 0, 0, 0])
            >>> covariance = np.eye(8)
            >>> predicted_mean, predicted_covariance = kf.predict(mean, covariance)
        '''
        mean = self._motion_mat @ mean
        std_pos = self._std_weight_position * mean[3]
        std_vel = self._std_weight_velocity * mean[3]
        motion_cov = np.diag(
            np.array([std_pos, std_pos, std_pos, std_pos, std_vel,
                     std_vel, std_vel, std_vel], dtype=np.float32) ** 2
        )
        covariance = self._motion_mat @ covariance @ self._motion_mat.T + motion_cov
        return mean.astype(np.float32), covariance.astype(np.float32)

    def project(self, mean: np.ndarray, covariance: np.ndarray) -> tuple:
        '''
        Project state distribution to measurement space.
        Args:
            mean (ndarray): The state's mean vector (8 dimensional array).
            covariance (ndarray): The state's covariance matrix (8x8 dimensional).
        Returns:
            (tuple[ndarray, ndarray]): Returns the projected mean and covariance matrix of the given state estimate.
        Examples:
            >>> kf = KalmanFilterXYAH()
            >>> mean = np.array([0, 0, 1, 1, 0, 0, 0, 0])
            >>> covariance = np.eye(8)
            >>> projected_mean, projected_covariance = kf.project(mean, covariance)
        '''
        proj_mean = self._update_mat @ mean
        std = self._std_weight_position * mean[3]
        innovation_cov = np.diag(
            np.array([std, std, std, std], dtype=np.float32) ** 2)
        proj_cov = self._update_mat @ covariance @ self._update_mat.T + innovation_cov
        return proj_mean.astype(np.float32), proj_cov.astype(np.float32)

    def multi_predict(self, mean: np.ndarray, covariance: np.ndarray) -> tuple:
        '''
        Run Kalman filter prediction step for multiple object states (Vectorized version).
        Args:
            mean (ndarray): The Nx8 dimensional mean matrix of the object states at the previous time step.
            covariance (ndarray): The Nx8x8 covariance matrix of the object states at the previous time step.
        Returns:
            (tuple[ndarray, ndarray]): Returns the mean matrix and covariance matrix of the predicted states.
                The mean matrix has shape (N, 8) and the covariance matrix has shape (N, 8, 8). Unobserved velocities
                are initialized to 0 mean.
        Examples:
            >>> mean = np.random.rand(10, 8)  # 10 object states
            >>> covariance = np.random.rand(10, 8, 8)  # Covariance matrices for 10 object states
            >>> predicted_mean, predicted_covariance = kalman_filter.multi_predict(mean, covariance)
        '''
        F = self._motion_mat.astype(np.float32)
        means = mean @ F.T

        std_pos = self._std_weight_position * means[:, 3]
        std_vel = self._std_weight_velocity * means[:, 3]
        q_diag = np.stack(
            [std_pos**2, std_pos**2, std_pos**2, std_pos**2,
                std_vel**2, std_vel**2, std_vel**2, std_vel**2],
            axis=1,
        ).astype(np.float32)

        # Covariance prediction: F P F^T + Q, batched
        FP = np.einsum('ij,njk->nik', F, covariance)
        # note: einsum broadcasting across shared second index
        covs = np.einsum('nij,kj->nik', FP, F.T)
        # The above line with 'nij,kj->nik' uses F.T shared across batches; expand explicitly:
        covs = np.einsum('nij,lj->nil', FP, F.T)
        covs = covs + np.einsum('ni,nj->nij', q_diag, np.ones(8,
                                dtype=np.float32)) * np.eye(8, dtype=np.float32)

        return means.astype(np.float32), covs.astype(np.float32)

    def update(self, mean: np.ndarray, covariance: np.ndarray, measurement: np.ndarray) -> tuple:
        '''
        Run Kalman filter correction step.
        Args:
            mean (ndarray): The predicted state's mean vector (8 dimensional).
            covariance (ndarray): The state's covariance matrix (8x8 dimensional).
            measurement (ndarray): The 4 dimensional measurement vector (x, y, a, h), where (x, y) is the center
                position, a the aspect ratio, and h the height of the bounding box.
        Returns:
            (tuple[ndarray, ndarray]): Returns the measurement-corrected state distribution.
        Examples:
            >>> kf = KalmanFilterXYAH()
            >>> mean = np.array([0, 0, 1, 1, 0, 0, 0, 0])
            >>> covariance = np.eye(8)
            >>> measurement = np.array([1, 1, 1, 1])
            >>> new_mean, new_covariance = kf.update(mean, covariance, measurement)
        '''
        H = self._update_mat
        proj_mean, S = self.project(mean, covariance)
        y = (measurement.astype(np.float32) - proj_mean).astype(np.float32)

        # Kalman gain using solve for numerical stability
        HP = H @ covariance
        K = np.linalg.solve(S, HP).T  # shape (8,4)

        new_mean = mean + K @ y
        new_cov = covariance - K @ S @ K.T

        return new_mean.astype(np.float32), new_cov.astype(np.float32)

    def gating_distance(self, mean: np.ndarray, covariance: np.ndarray, measurements: np.ndarray, only_position: bool = False, metric: str = 'maha') -> np.ndarray:
        '''
        Compute gating distance between state distribution and measurements.
        A suitable distance threshold can be obtained from `chi2inv95`. If `only_position` is False, the chi-square
        distribution has 4 degrees of freedom, otherwise 2.
        Args:
            mean (ndarray): Mean vector over the state distribution (8 dimensional).
            covariance (ndarray): Covariance of the state distribution (8x8 dimensional).
            measurements (ndarray): An (N, 4) matrix of N measurements, each in format (x, y, a, h) where (x, y) is the
                bounding box center position, a the aspect ratio, and h the height.
            only_position (bool): If True, distance computation is done with respect to box center position only.
            metric (str): The metric to use for calculating the distance. Options are 'gaussian' for the squared
                Euclidean distance and 'maha' for the squared Mahalanobis distance.
        Returns:
            (np.ndarray): Returns an array of length N, where the i-th element contains the squared distance between
                (mean, covariance) and `measurements[i]`.
        Examples:
            Compute gating distance using Mahalanobis metric:
            >>> kf = KalmanFilterXYAH()
            >>> mean = np.array([0, 0, 1, 1, 0, 0, 0, 0])
            >>> covariance = np.eye(8)
            >>> measurements = np.array([[1, 1, 1, 1], [2, 2, 1, 1]])
            >>> distances = kf.gating_distance(mean, covariance, measurements, only_position=False, metric="maha")
        '''
        if measurements.size == 0:
            return np.zeros((0,), dtype=np.float32)

        H = self._update_mat
        if only_position:
            H = H[:2, :]
        proj_mean = (H @ mean).astype(np.float32)
        S_base = H @ covariance @ H.T

        if only_position:
            std = self._std_weight_position * mean[3]
            R = np.diag(np.array([std, std], dtype=np.float32) ** 2)
        else:
            std = self._std_weight_position * mean[3]
            R = np.diag(np.array([std, std, std, std], dtype=np.float32) ** 2)

        S = (S_base + R).astype(np.float32)

        y = measurements.astype(np.float32) - proj_mean
        if only_position:
            y = y[:, :2]

        if metric == 'gaussian':
            d2 = np.einsum('ni,ni->n', y, y)
            return d2.astype(np.float32)

        if metric != 'maha':
            raise ValueError("metric must be 'maha' or 'gaussian'")

        # Mahalanobis distance with Cholesky
        try:
            L = np.linalg.cholesky(S)
        except np.linalg.LinAlgError:
            # Fallback to pseudo-inverse if not positive definite
            S_inv = np.linalg.pinv(S)
            d2 = np.einsum('ni,ij,nj->n', y, S_inv, y)
            return d2.astype(np.float32)

        # Solve L v = y^T -> v, then L^T w = v -> w; distance^2 = sum(w^2)
        v = np.linalg.solve(L, y.T)          # shape (m, N)
        w = np.linalg.solve(L.T, v)          # shape (m, N)
        d2 = np.sum(w * w, axis=0)           # length N
        return d2.astype(np.float32)
