class VelocityIndicator:
    '''Velocity indicator component for burn rate visualization.'''

    @staticmethod
    def get_velocity_emoji(burn_rate: float) -> str:
        '''Get velocity emoji based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Emoji representing velocity level
        '''
        if burn_rate < 100:
            return "🐢"
        elif burn_rate < 500:
            return "🚶"
        elif burn_rate < 2000:
            return "🏃"
        elif burn_rate < 10000:
            return "🚗"
        elif burn_rate < 50000:
            return "🚀"
        else:
            return "🌪️"

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        '''Get velocity description based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Text description of velocity level
        '''
        if burn_rate < 100:
            return "Very Low"
        elif burn_rate < 500:
            return "Low"
        elif burn_rate < 2000:
            return "Moderate"
        elif burn_rate < 10000:
            return "High"
        elif burn_rate < 50000:
            return "Very High"
        else:
            return "Extreme"

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        '''Render velocity indicator.
        Args:
            burn_rate: Token burn rate per minute
            include_description: Whether to include text description
        Returns:
            Formatted velocity indicator
        '''
        emoji = VelocityIndicator.get_velocity_emoji(burn_rate)
        if include_description:
            desc = VelocityIndicator.get_velocity_description(burn_rate)
            return f"{emoji} {desc} ({burn_rate:.0f}/min)"
        else:
            return f"{emoji} {burn_rate:.0f}/min"
