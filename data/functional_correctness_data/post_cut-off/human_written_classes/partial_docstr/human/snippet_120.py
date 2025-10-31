import torch
import numpy as np
import torch.utils.cpp_extension

class SensorPose3DModel:

    def __init__(self, R, T, trans=np.array([0.0, 0.0, 0.0]), scale=1.0):
        super(SensorPose3DModel, self).__init__()
        self.R = R
        self.T = T
        self.zfar = 100.0
        self.znear = 0.01
        self.trans = trans
        self.scale = scale
        self.world_view_transform = torch.tensor(SensorPose3DModel.__getWorld2View2(R, T, trans, scale)).transpose(0, 1).cpu()

    @staticmethod
    def __getWorld2View2(R, t, translate=np.array([0.0, 0.0, 0.0]), scale=1.0):
        Rt = np.zeros((4, 4))
        Rt[:3, :3] = R.transpose()
        Rt[:3, 3] = t
        Rt[3, 3] = 1.0
        C2W = np.linalg.inv(Rt)
        cam_center = C2W[:3, 3]
        cam_center = (cam_center + translate) * scale
        C2W[:3, 3] = cam_center
        Rt = np.linalg.inv(C2W)
        return np.float32(Rt)

    @staticmethod
    def __so3_matrix_to_quat(R: torch.Tensor | np.ndarray, unbatch: bool=True) -> torch.Tensor:
        """
        Converts a singe / batch of SO3 rotation matrices (3x3) to unit quaternion representation.

        Args:
            R: single / batch of SO3 rotation matrices [bs, 3, 3] or [3,3]
            unbatch: if the single example should be unbatched (first dimension removed) or not

        Returns:
            single / batch of unit quaternions (XYZW convention)  [bs, 4] or [4]
        """
        if isinstance(R, np.ndarray):
            R = torch.from_numpy(R)
        R = R.reshape((-1, 3, 3))
        num_rotations, D1, D2 = R.shape
        assert (D1, D2) == (3, 3), 'so3_matrix_to_quat: Input has to be a Bx3x3 tensor.'
        decision_matrix = torch.empty((num_rotations, 4), dtype=R.dtype, device=R.device)
        quat = torch.empty((num_rotations, 4), dtype=R.dtype, device=R.device)
        decision_matrix[:, :3] = R.diagonal(dim1=1, dim2=2)
        decision_matrix[:, -1] = decision_matrix[:, :3].sum(dim=1)
        choices = decision_matrix.argmax(dim=1)
        ind = torch.nonzero(choices != 3, as_tuple=True)[0]
        i = choices[ind]
        j = (i + 1) % 3
        k = (j + 1) % 3
        quat[ind, i] = 1 - decision_matrix[ind, -1] + 2 * R[ind, i, i]
        quat[ind, j] = R[ind, j, i] + R[ind, i, j]
        quat[ind, k] = R[ind, k, i] + R[ind, i, k]
        quat[ind, 3] = R[ind, k, j] - R[ind, j, k]
        ind = torch.nonzero(choices == 3, as_tuple=True)[0]
        quat[ind, 0] = R[ind, 2, 1] - R[ind, 1, 2]
        quat[ind, 1] = R[ind, 0, 2] - R[ind, 2, 0]
        quat[ind, 2] = R[ind, 1, 0] - R[ind, 0, 1]
        quat[ind, 3] = 1 + decision_matrix[ind, -1]
        quat = quat / torch.norm(quat, dim=1)[:, None]
        if unbatch:
            quat = quat.squeeze()
        return quat

    def get_sensor_pose(self):
        T_world_sensor_t = self.world_view_transform[3, :3]
        T_world_sensor_R = self.world_view_transform[:3, :3].transpose(0, 1)
        T_world_sensor_quat = SensorPose3DModel.__so3_matrix_to_quat(T_world_sensor_R)
        T_world_sensor_tquat = torch.hstack([T_world_sensor_t.cpu(), T_world_sensor_quat.cpu()])
        return SensorPose3D(T_world_sensors=[T_world_sensor_tquat, T_world_sensor_tquat], timestamps_us=[0, 1])