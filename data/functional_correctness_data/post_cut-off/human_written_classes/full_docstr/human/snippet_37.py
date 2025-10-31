from claude_monitor.terminal.themes import get_cost_style, get_velocity_indicator

class VelocityIndicator:
    """Velocity indicator component for burn rate visualization."""

    @staticmethod
    def get_velocity_emoji(burn_rate: float) -> str:
        """Get velocity emoji based on burn rate.

        Args:
            burn_rate: Token burn rate per minute

        Returns:
            Emoji representing velocity level
        """
        indicator = get_velocity_indicator(burn_rate)
        return indicator['emoji']

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        """Get velocity description based on burn rate.

        Args:
            burn_rate: Token burn rate per minute

        Returns:
            Text description of velocity level
        """
        indicator = get_velocity_indicator(burn_rate)
        return indicator['label']

    @staticmethod
    def render(burn_rate: float, include_description: bool=False) -> str:
        """Render velocity indicator.

        Args:
            burn_rate: Token burn rate per minute
            include_description: Whether to include text description

        Returns:
            Formatted velocity indicator
        """
        emoji = VelocityIndicator.get_velocity_emoji(burn_rate)
        if include_description:
            description = VelocityIndicator.get_velocity_description(burn_rate)
            return f'{emoji} {description}'
        return emoji