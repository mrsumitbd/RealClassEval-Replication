import xrobotoolkit_sdk as xrt
import numpy as np

class XrClient:
    """Client for the XrClient SDK to interact with XR devices."""

    def __init__(self):
        """Initializes the XrClient and the SDK."""
        xrt.init()

    def get_pose_by_name(self, name: str) -> np.ndarray:
        """Returns the pose of the specified device by name.
        Valid names: "left_controller", "right_controller", "headset".
        Pose is [x, y, z, qx, qy, qz, qw]."""
        if name == 'left_controller':
            return xrt.get_left_controller_pose()
        elif name == 'right_controller':
            return xrt.get_right_controller_pose()
        elif name == 'headset':
            return xrt.get_headset_pose()
        else:
            raise ValueError(f"Invalid name: {name}. Valid names are: 'left_controller', 'right_controller', 'headset'.")

    def get_key_value_by_name(self, name: str) -> float:
        """Returns the trigger/grip value by name (float).
        Valid names: "left_trigger", "right_trigger", "left_grip", "right_grip".
        """
        if name == 'left_trigger':
            return xrt.get_left_trigger()
        elif name == 'right_trigger':
            return xrt.get_right_trigger()
        elif name == 'left_grip':
            return xrt.get_left_grip()
        elif name == 'right_grip':
            return xrt.get_right_grip()
        else:
            raise ValueError(f"Invalid name: {name}. Valid names are: 'left_trigger', 'right_trigger', 'left_grip', 'right_grip'.")

    def get_button_state_by_name(self, name: str) -> bool:
        """Returns the button state by name (bool).
        Valid names: "A", "B", "X", "Y",
                      "left_menu_button", "right_menu_button",
                      "left_axis_click", "right_axis_click"
        """
        if name == 'A':
            return xrt.get_A_button()
        elif name == 'B':
            return xrt.get_B_button()
        elif name == 'X':
            return xrt.get_X_button()
        elif name == 'Y':
            return xrt.get_Y_button()
        elif name == 'left_menu_button':
            return xrt.get_left_menu_button()
        elif name == 'right_menu_button':
            return xrt.get_right_menu_button()
        elif name == 'left_axis_click':
            return xrt.get_left_axis_click()
        elif name == 'right_axis_click':
            return xrt.get_right_axis_click()
        else:
            raise ValueError(f"Invalid name: {name}. Valid names are: 'A', 'B', 'X', 'Y', 'left_menu_button', 'right_menu_button', 'left_axis_click', 'right_axis_click'.")

    def get_timestamp_ns(self) -> int:
        """Returns the current timestamp in nanoseconds (int)."""
        return xrt.get_time_stamp_ns()

    def close(self):
        xrt.close()