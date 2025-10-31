import torch
from typing import Dict
from isaacsim.core.prims import RigidPrim
from simulation.environments.state_machine.utils import SMState, compute_relative_action
from simulation.environments.state_machine.modules.base_module import BaseControlModule

class UltrasoundStateMachine:
    """State machine for ultrasound procedure control."""

    def __init__(self, modules: Dict[str, BaseControlModule], device: str='cuda:0'):
        """Initialize the state machine.

        Args:
            modules (Dict[str, BaseControlModule]): Dictionary of control modules
            device (str): Device to run computations on
        """
        self.modules = modules
        self.device = device
        self.sm_state = SMState()
        self.object_view = RigidPrim(prim_paths_expr='/World/envs/env.*/Robot/panda_hand', name='robot', track_contact_forces=True, prepare_contact_sensors=True, contact_filter_prim_paths_expr=['/World/envs/env.*/organs'], max_contact_count=50)
        self.object_view.initialize()
        self.assert_module_order()

    def compute_action(self, env, robot_obs: torch.Tensor) -> torch.Tensor:
        """Compute combined action from all active modules.

        Args:
            env: The environment instance
            robot_obs: Current robot observations

        Returns:
            Tuple of relative and absolute commands
        """
        self.sm_state.robot_obs = robot_obs
        self.sm_state.contact_normal_force = self.get_normal_force()
        module_actions = {}
        for name, module in self.modules.items():
            action, state = module.compute_action(env, self.sm_state)
            module_actions[name] = action
            self.sm_state = state
        abs_commands = sum(module_actions.values())
        rel_commands = compute_relative_action(abs_commands, robot_obs.unsqueeze(0))
        return (rel_commands, abs_commands)

    def get_normal_force(self):
        """
        Get the average normal force from the contact sensor.
        """
        contact_forces = self.object_view.get_contact_force_data()[2]
        non_zero_mask = torch.all(contact_forces == 0, dim=1).logical_not()
        force_sum = contact_forces[non_zero_mask].sum(dim=0)
        num_non_zero = non_zero_mask.sum()
        mean_force = force_sum / num_non_zero if num_non_zero > 0 else torch.zeros(3, device=contact_forces.device)
        return mean_force

    def reset(self) -> None:
        """Reset the state machine and all modules."""
        self.sm_state.reset()
        for module in self.modules.values():
            module.reset()

    def assert_module_order(self):
        """Assert that the modules are in the correct order."""
        assert list(self.modules.keys()) == ['force', 'orientation', 'path_planning'], 'Modules must be in the correct order'