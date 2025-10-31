
class CkClass:
    def __init__(self, flags, state):
        """
        Initialize the CkClass instance.

        Args:
            flags (int): The flags value.
            state (int): The state value.
        """
        self.flags = flags
        self.state = state

    def flags2text(self):
        """
        Convert flags to text representation.

        Returns:
            str: Text representation of the flags.
        """
        flag_map = {
            0: "None",
            1: "Flag1",
            2: "Flag2",
            4: "Flag3",
            # Add more flag mappings as needed
        }
        flag_text = []
        for flag, text in flag_map.items():
            if self.flags & flag:
                flag_text.append(text)
        return ", ".join(flag_text) if flag_text else "None"

    def state2text(self):
        """
        Convert state to text representation.

        Returns:
            str: Text representation of the state.
        """
        state_map = {
            0: "State0",
            1: "State1",
            2: "State2",
            # Add more state mappings as needed
        }
        return state_map.get(self.state, "Unknown")

    def to_dict(self):
        """
        Convert the CkClass instance to a dictionary.

        Returns:
            dict: Dictionary representation of the CkClass instance.
        """
        return {
            "flags": self.flags,
            "flags_text": self.flags2text(),
            "state": self.state,
            "state_text": self.state2text(),
        }

    def __str__(self):
        """
        Return a string representation of the CkClass instance.

        Returns:
            str: String representation of the CkClass instance.
        """
        return f"CkClass(flags={self.flags} ({self.flags2text()}), state={self.state} ({self.state2text()}))"


# Example usage:
if __name__ == "__main__":
    ck_instance = CkClass(flags=3, state=1)
    print(ck_instance)
    print(ck_instance.to_dict())
