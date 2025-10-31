class VelocityIndicator:
    '''Velocity indicator component for burn rate visualization.'''

    # Thresholds in tokens/minute: (upper_bound_inclusive, emoji, description)
    _LEVELS = [
        (0.0, "⏸️", "Paused"),
        (100.0, "🐢", "Low velocity"),
        (500.0, "🚶", "Moderate velocity"),
        (1500.0, "🏃", "High velocity"),
        (5000.0, "🚀", "Very high velocity"),
        (float("inf"), "🔥", "Extreme velocity"),
    ]

    @staticmethod
    def _is_finite(value: float) -> bool:
        try:
            return float("-inf") < float(value) < float("inf")
        except Exception:
            return False

    @staticmethod
    def _classify(burn_rate: float):
        if not VelocityIndicator._is_finite(burn_rate):
            return "❓", "Unknown velocity"
        # Treat negatives as zero activity
        rate = max(0.0, float(burn_rate))
        for upper, emoji, desc in VelocityIndicator._LEVELS:
            if rate <= upper:
                return emoji, desc
        # Fallback (should not reach due to inf bound)
        return "❓", "Unknown velocity"

    @staticmethod
    def get_velocity_emoji(burn_rate: float) -> str:
        '''Get velocity emoji based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Emoji representing velocity level
        '''
        emoji, _ = VelocityIndicator._classify(burn_rate)
        return emoji

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        '''Get velocity description based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Text description of velocity level
        '''
        _, desc = VelocityIndicator._classify(burn_rate)
        return desc

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        '''Render velocity indicator.
        Args:
            burn_rate: Token burn rate per minute
            include_description: Whether to include text description
        Returns:
            Formatted velocity indicator
        '''
        emoji, desc = VelocityIndicator._classify(burn_rate)
        if include_description:
            if VelocityIndicator._is_finite(burn_rate):
                return f"{emoji} {desc} ({max(0.0, float(burn_rate)):.0f}/min)"
            else:
                return f"{emoji} {desc}"
        return emoji
