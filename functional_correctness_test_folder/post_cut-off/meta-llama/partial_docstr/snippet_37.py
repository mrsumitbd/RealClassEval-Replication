
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
        if burn_rate < 0.1:
            return '🛑'
        elif burn_rate < 1:
            return '🐌'
        elif burn_rate < 10:
            return '🚶‍♂️'
        elif burn_rate < 100:
            return '🏃‍♂️'
        else:
            return '🚀'

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        '''Get velocity description based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Description representing velocity level
        '''
        if burn_rate < 0.1:
            return 'Very Low'
        elif burn_rate < 1:
            return 'Low'
        elif burn_rate < 10:
            return 'Moderate'
        elif burn_rate < 100:
            return 'High'
        else:
            return 'Very High'

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        '''Render velocity indicator component.
        Args:
            burn_rate: Token burn rate per minute
            include_description: Whether to include velocity description
        Returns:
            Rendered velocity indicator component
        '''
        emoji = VelocityIndicator.get_velocity_emoji(burn_rate)
        if include_description:
            description = VelocityIndicator.get_velocity_description(burn_rate)
            return f'{emoji} {description}'
        else:
            return emoji
