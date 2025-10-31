
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
            return '🐌'
        elif 0.1 <= burn_rate < 0.5:
            return '🚶‍♂️'
        elif 0.5 <= burn_rate < 1.0:
            return '🏃‍♂️'
        elif 1.0 <= burn_rate < 2.0:
            return '💨'
        else:
            return '🔥'

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        '''Get velocity description based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Text description of velocity level
        '''
        if burn_rate < 0.1:
            return 'Very Slow'
        elif 0.1 <= burn_rate < 0.5:
            return 'Slow'
        elif 0.5 <= burn_rate < 1.0:
            return 'Moderate'
        elif 1.0 <= burn_rate < 2.0:
            return 'Fast'
        else:
            return 'Very Fast'

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
            description = VelocityIndicator.get_velocity_description(burn_rate)
            return f'{emoji} {description}'
        return emoji
