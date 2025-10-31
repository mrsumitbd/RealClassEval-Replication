import math


class VelocityIndicator:
    '''Velocity indicator component for burn rate visualization.'''
    @staticmethod
    def _normalize_rate(burn_rate: float) -> float:
        try:
            rate = float(burn_rate)
        except (TypeError, ValueError):
            raise ValueError("burn_rate must be a number")
        if math.isnan(rate) or math.isinf(rate):
            return 0.0 if math.isnan(rate) else float('inf')
        return max(rate, 0.0)

    @staticmethod
    def get_velocity_emoji(burn_rate: float) -> str:
        '''Get velocity emoji based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Emoji representing velocity level
        '''
        rate = VelocityIndicator._normalize_rate(burn_rate)
        if rate == 0:
            return '💤'
        if rate < 200:
            return '🐢'
        if rate < 800:
            return '🚶'
        if rate < 2000:
            return '🏃'
        if rate < 5000:
            return '🚀'
        return '☄️'

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        '''Get velocity description based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Text description of velocity level
        '''
        rate = VelocityIndicator._normalize_rate(burn_rate)
        if rate == 0:
            return 'Idle'
        if rate < 200:
            return 'Slow'
        if rate < 800:
            return 'Moderate'
        if rate < 2000:
            return 'Fast'
        if rate < 5000:
            return 'Very Fast'
        return 'Extreme'

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
