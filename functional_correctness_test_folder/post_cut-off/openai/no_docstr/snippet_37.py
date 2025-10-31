
class VelocityIndicator:
    """
    Utility class for representing a burn rate with an emoji and a textual description.
    """

    @staticmethod
    def get_velocity_emoji(burn_rate: float) -> str:
        """
        Return an emoji that represents the speed of the burn rate.

        Parameters
        ----------
        burn_rate : float
            A numeric value representing the burn rate.  The value is interpreted
            relative to the following thresholds:

            * 0.0 – 0.3   → slow (🐢)
            * 0.3 – 0.7   → medium (🐇)
            * 0.7 – 1.0+  → fast (🚀)

        Returns
        -------
        str
            The chosen emoji.
        """
        if burn_rate <= 0.3:
            return "🐢"
        if burn_rate <= 0.7:
            return "🐇"
        return "🚀"

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        """
        Return a short textual description of the burn rate.

        Parameters
        ----------
        burn_rate : float
            Same interpretation as in :meth:`get_velocity_emoji`.

        Returns
        -------
        str
            A human‑readable description.
        """
        if burn_rate <= 0.3:
            return "Slow burn"
        if burn_rate <= 0.7:
            return "Steady burn"
        return "Rapid burn"

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        """
        Render the velocity indicator as a string.

        Parameters
        ----------
        burn_rate : float
            The burn rate value.
        include_description : bool, optional
            If ``True``, append the description after the emoji.

        Returns
        -------
        str
            The rendered indicator.
        """
        emoji = VelocityIndicator.get_velocity_emoji(burn_rate)
        if include_description:
            description = VelocityIndicator.get_velocity_description(burn_rate)
            return f"{emoji} {description}"
        return emoji
