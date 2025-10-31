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
        try:
            r = float(burn_rate)
        except (TypeError, ValueError):
            r = 0.0

        if r <= 0 or r != r:  # NaN or non-positive
            return '💤'
        if r == float('inf'):
            return '🔥'
        if r < 100:
            return '🐢'
        if r < 500:
            return '🚶'
        if r < 1500:
            return '🏃'
        if r < 5000:
            return '🚀'
        return '🔥'

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        '''Get velocity description based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Text description of velocity level
        '''
        try:
            r = float(burn_rate)
        except (TypeError, ValueError):
            r = 0.0

        if r <= 0 or r != r:
            return 'idle'
        if r == float('inf'):
            return 'extreme'
        if r < 100:
            return 'low'
        if r < 500:
            return 'moderate'
        if r < 1500:
            return 'high'
        if r < 5000:
            return 'very high'
        return 'extreme'

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
        desc = VelocityIndicator.get_velocity_description(burn_rate)

        try:
            r = float(burn_rate)
        except (TypeError, ValueError):
            r = 0.0

        if r == float('inf'):
            rate_str = '∞'
        else:
            if r >= 100:
                rate_str = f'{r:,.0f}'
            elif r >= 10:
                rate_str = f'{r:,.1f}'
            else:
                rate_str = f'{r:,.2f}'

        base = f'{emoji} {rate_str} tpm'
        if include_description:
            return f'{base} - {desc} velocity'
        return base
