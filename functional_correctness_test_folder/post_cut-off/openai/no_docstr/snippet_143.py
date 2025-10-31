
from typing import Optional


class RobustnessType:
    """Simple enumeration of robustness vulnerability types."""
    INPUT_OVERRELIANCE = "input_overreliance"
    HIJACKING = "hijacking"
    OTHER = "other"


class RobustnessTemplate:
    @staticmethod
    def generate_baseline_attacks(
        vulnerability_type: RobustnessType,
        max_goldens: int,
        purpose: Optional[str] = None
    ) -> str:
        """
        Generate a baseline attack string for the given vulnerability type.

        Parameters
        ----------
        vulnerability_type : RobustnessType
            The type of vulnerability to generate attacks for.
        max_goldens : int
            Maximum number of golden examples to include in the attack.
        purpose : Optional[str]
            Optional purpose or description to include in the output.

        Returns
        -------
        str
            A formatted string describing the baseline attacks.
        """
        if vulnerability_type == RobustnessType.INPUT_OVERRELIANCE:
            return RobustnessTemplate.generate_input_overreliance_baseline_attacks(
                max_goldens, purpose
            )
        if vulnerability_type == RobustnessType.HIJACKING:
            return RobustnessTemplate.generate_hijacking_baseline_attacks(
                max_goldens, purpose
            )
        # Default fallback
        attacks = [
            f"Generic attack {i+1}" for i in range(min(max_goldens, 5))
        ]
        desc = f"Baseline attacks for {vulnerability_type}"
        if purpose:
            desc += f" ({purpose})"
        return f"{desc}:\n" + "\n".join(attacks)

    @staticmethod
    def generate_input_overreliance_baseline_attacks(
        max_goldens: int,
        purpose: Optional[str] = None
    ) -> str:
        """
        Generate baseline attacks for input overreliance vulnerability.

        Parameters
        ----------
        max_goldens : int
            Maximum number of golden examples to include.
        purpose : Optional[str]
            Optional purpose or description to include.

        Returns
        -------
        str
            A formatted string describing the input overreliance attacks.
        """
        attacks = [
            f"Overreliance attack {i+1}" for i in range(min(max_goldens, 5))
        ]
        desc = "Baseline input overreliance attacks"
        if purpose:
            desc += f" ({purpose})"
        return f"{desc}:\n" + "\n".join(attacks)

    @staticmethod
    def generate_hijacking_baseline_attacks(
        max_goldens: int,
        purpose: Optional[str] = None
    ) -> str:
        """
        Generate baseline attacks for hijacking vulnerability.

        Parameters
        ----------
        max_goldens : int
            Maximum number of golden examples to include.
        purpose : Optional[str]
            Optional purpose or description to include.

        Returns
        -------
        str
            A formatted string describing the hijacking attacks.
        """
        attacks = [
            f"Hijacking attack {i+1}" for i in range(min(max_goldens, 5))
        ]
        desc = "Baseline hijacking attacks"
        if purpose:
            desc += f" ({purpose})"
        return f"{desc}:\n" + "\n".join(attacks)
