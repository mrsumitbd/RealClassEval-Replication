
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
        if burn_rate < 0:
            return '❓'
        if burn_rate < 1:
            return '🐢'   # very slow
        if burn_rate < 5:
            return '🐇'   # moderate
        return '🚀'       # fast

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        '''Get velocity description based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Text description of velocity level
        '''
        if burn_rate < 0:
            return 'Unknown burn rate'
        if burn_rate < 1:
            return 'Very slow burn'
        if burn_rate < 5:
            return 'Moderate burn'
        return 'Fast burn'

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
