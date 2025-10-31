from collections.abc import Sequence
import torch
import warp as wp

class ReachSm:
    """A simple state machine in a robot's task space for a reach task.

    The state machine is implemented as a warp kernel. It takes in the current state of
    the robot's end-effector, and outputs the desired state of the robot's end-effector.
    The state machine is implemented as a finite state machine with the following states:

    1. REST: The robot is at rest.
    2. REACH: The robot reaches to the desired pose. This is the final state.
    """

    def __init__(self, dt: float, num_envs: int, device: torch.device | str='cpu'):
        """Initialize the state machine.

        Args:
            dt: The environment time step.
            num_envs: The number of environments to simulate.
            device: The device to run the state machine on.
        """
        self.dt = float(dt)
        self.num_envs = num_envs
        self.device = device
        self.sm_dt = torch.full((self.num_envs,), self.dt, device=self.device)
        self.sm_state = torch.full((self.num_envs,), 0, dtype=torch.int32, device=self.device)
        self.sm_wait_time = torch.zeros((self.num_envs,), device=self.device)
        self.des_ee_1_pose = torch.zeros((self.num_envs, 7), device=self.device)
        self.des_ee_2_pose = torch.zeros((self.num_envs, 7), device=self.device)
        self.sm_dt_wp = wp.from_torch(self.sm_dt, wp.float32)
        self.sm_state_wp = wp.from_torch(self.sm_state, wp.int32)
        self.sm_wait_time_wp = wp.from_torch(self.sm_wait_time, wp.float32)
        self.des_ee_1_pose_wp = wp.from_torch(self.des_ee_1_pose, wp.transform)
        self.des_ee_2_pose_wp = wp.from_torch(self.des_ee_2_pose, wp.transform)

    def reset_idx(self, env_ids: Sequence[int]=None):
        """Reset the state machine."""
        if env_ids is None:
            env_ids = slice(None)
        self.sm_state[env_ids] = 0
        self.sm_wait_time[env_ids] = 0.0

    def compute(self, ee_1_pose: torch.Tensor, ee_2_pose: torch.Tensor, des_final_pose_1: torch.Tensor, des_final_pose_2: torch.Tensor):
        """Compute the desired state of the robot's end-effector."""
        ee_1_pose = ee_1_pose[:, [0, 1, 2, 4, 5, 6, 3]]
        ee_2_pose = ee_2_pose[:, [0, 1, 2, 4, 5, 6, 3]]
        des_final_pose_1 = des_final_pose_1[:, [0, 1, 2, 4, 5, 6, 3]]
        des_final_pose_2 = des_final_pose_2[:, [0, 1, 2, 4, 5, 6, 3]]
        ee_1_pose_wp = wp.from_torch(ee_1_pose.contiguous(), wp.transform)
        ee_2_pose_wp = wp.from_torch(ee_2_pose.contiguous(), wp.transform)
        des_final_pose_1_wp = wp.from_torch(des_final_pose_1.contiguous(), wp.transform)
        des_final_pose_2_wp = wp.from_torch(des_final_pose_2.contiguous(), wp.transform)
        wp.launch(kernel=infer_state_machine, dim=self.num_envs, inputs=[self.sm_dt_wp, self.sm_state_wp, self.sm_wait_time_wp, ee_1_pose_wp, ee_2_pose_wp, des_final_pose_1_wp, des_final_pose_2_wp, self.des_ee_1_pose_wp, self.des_ee_2_pose_wp], device=self.device)
        des_ee_1_pose = self.des_ee_1_pose[:, [0, 1, 2, 6, 3, 4, 5]]
        des_ee_2_pose = self.des_ee_2_pose[:, [0, 1, 2, 6, 3, 4, 5]]
        return torch.cat([des_ee_1_pose, des_ee_2_pose], dim=-1)