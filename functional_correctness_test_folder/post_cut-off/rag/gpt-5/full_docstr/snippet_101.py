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
        self._motion_mat = np.eye(2 * ndim, dtype=np.float32)
        for i in range(ndim):
            self._motion_mat[i, ndim + i] = dt

        self._update_mat = np.zeros((ndim, 2 * ndim), dtype=np.float32)
        self._update_mat[:ndim, :ndim] = np.eye(ndim, dtype=np.float32)

        self._std_weight_position = 1.0 / 20.0
        self._std_weight_velocity = 1.0 / 160.0

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
        std = np.array([
            2.0 * self._std_weight_position * h,
            2.0 * self._std_weight_position * h,
            1e-2,
            2.0 * self._std_weight_position * h,
            10.0 * self._std_weight_velocity * h,
            10.0 * self._std_weight_velocity * h,
            1e-5,
            10.0 * self._std_weight_velocity * h
        ], dtype=np.float32)

        covariance = np.diag(std ** 2).astype(np.float32)
        return mean, covariance

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
        mean = (self._motion_mat @ mean.astype(np.float32)).astype(np.float32)

        h = float(mean[3])
        std_pos = np.array([
            self._std_weight_position * h,
            self._std_weight_position * h,
            1e-2,
            self._std_weight_position * h
        ], dtype=np.float32)
        std_vel = np.array([
            self._std_weight_velocity * h,
            self._std_weight_velocity * h,
            1e-5,
            self._std_weight_velocity * h
        ], dtype=np.float32)
        motion_cov_diag = np.concatenate([std_pos, std_vel]).astype(np.float32)
        Q = np.diag(motion_cov_diag ** 2).astype(np.float32)

        covariance = (self._motion_mat @ covariance @
                      self._motion_mat.T + Q).astype(np.float32)
        return mean, covariance

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
        mean = mean.astype(np.float32)
        covariance = covariance.astype(np.float32)

        proj_mean = (self._update_mat @ mean).astype(np.float32)

        h = float(mean[3])
        std = np.array([
            self._std_weight_position * h,
            self._std_weight_position * h,
            1e-2,
            self._std_weight_position * h
        ], dtype=np.float32)
        R = np.diag(std ** 2).astype(np.float32)

        proj_cov = (self._update_mat @ covariance @
                    self._update_mat.T + R).astype(np.float32)
        return proj_mean, proj_cov

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
        mean = mean.astype(np.float32)
        covariance = covariance.astype(np.float32)
        N = mean.shape[0]

        A = self._motion_mat.astype(np.float32)
        mean_pred = (mean @ A.T).astype(np.float32)

        h = mean_pred[:, 3].astype(np.float32)
        std_pos = np.stack([
            self._std_weight_position * h,
            self._std_weight_position * h,
            np.full_like(h, 1e-2, dtype=np.float32),
            self._std_weight_position * h
        ], axis=1).astype(np.float32)
        std_vel = np.stack([
            self._std_weight_velocity * h,
            self._std_weight_velocity * h,
            np.full_like(h, 1e-5, dtype=np.float32),
            self._std_weight_velocity * h
        ], axis=1).astype(np.float32)
        motion_cov_diag = np.concatenate(
            [std_pos, std_vel], axis=1).astype(np.float32)
        motion_cov_var = (motion_cov_diag ** 2).astype(np.float32)

        cov_pred = np.einsum('ij,njk,lk->nil', A,
                             covariance, A.T).astype(np.float32)
        idx = np.arange(8)
        cov_pred[:, idx, idx] += motion_cov_var
        return mean_pred, cov_pred

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
        mean = mean.astype(np.float32)
        covariance = covariance.astype(np.float32)
        measurement = measurement.astype(np.float32)

        proj_mean, proj_cov = self.project(mean, covariance)
        H = self._update_mat.astype(np.float32)

        PHT = covariance @ H.T
        try:
            # K = P H^T S^{-1} computed via solve for numerical stability
            K = np.linalg.solve(proj_cov, PHT.T).T.astype(np.float32)
        except np.linalg.LinAlgError:
            # Fallback to pseudo-inverse
            K = (PHT @ np.linalg.pinv(proj_cov)).astype(np.float32)

        innovation = (measurement - proj_mean).astype(np.float32)
        new_mean = (mean + K @ innovation).astype(np.float32)
        new_covariance = (covariance - K @ proj_cov @ K.T).astype(np.float32)
        new_covariance = 0.5 * \
            (new_covariance + new_covariance.T)  # ensure symmetry
        return new_mean, new_covariance

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
        proj_mean, proj_cov = self.project(mean.astype(
            np.float32), covariance.astype(np.float32))

        if only_position:
            idx = np.array([0, 1], dtype=int)
        else:
            idx = np.array([0, 1, 2, 3], dtype=int)

        mu = proj_mean[idx].astype(np.float32)
        S = proj_cov[np.ix_(idx, idx)].astype(np.float32)

        meas = measurements.astype(np.float32)
        d = meas[:, idx] - mu  # shape (N, d)

        if metric.lower() == 'gaussian':
            return np.sum(d ** 2, axis=1)

        if metric.lower() == 'maha':
            try:
                L = np.linalg.cholesky(S)  # S = L L^T
                # Solve L y = d^T -> y shape (dim, N)
                y = np.linalg.solve(L, d.T)
                return np.sum(y ** 2, axis=0)
            except np.linalg.LinAlgError:
                # Fallback to explicit inverse if S not PD
                S_inv = np.linalg.pinv(S)
                return np.einsum('ni,ij,nj->n', d, S_inv, d)

        raise ValueError(
            "Unknown metric '{}'. Use 'maha' or 'gaussian'.".format(metric))
