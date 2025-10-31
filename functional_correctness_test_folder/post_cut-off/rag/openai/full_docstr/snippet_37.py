
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
        # Define thresholds (tokens per minute)
        if burn_rate <= 5:
            return '🐢'   # Slow
        if burn_rate <= 15:
            return '🐇'   # Steady
        return '🚀'       # Fast

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        '''Get velocity description based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Text description of velocity level
        '''
        if burn_rate <= 5:
            return 'Slow'
        if burn_rate <= 15:
            return 'Steady'
        return 'Fast'

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
            return f'{emoji} {desc}'
        return emoji
