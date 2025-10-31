class VelocityIndicator:
    '''Velocity indicator component for burn rate visualization.'''
    @staticmethod
    def _normalize_rate(burn_rate: float) -> float:
        try:
            rate = float(burn_rate)
        except (TypeError, ValueError):
            rate = 0.0
        if rate != rate or rate < 0:  # NaN or negative
            rate = 0.0
        return rate

    @staticmethod
    def _format_rate(rate: float) -> str:
        if rate < 10:
            s = f"{rate:,.2f}"
        elif rate < 100:
            s = f"{rate:,.1f}"
        else:
            s = f"{rate:,.0f}"
        return s.rstrip('0').rstrip('.')

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
            return '⏸️'
        if rate < 10:
            return '🐢'
        if rate < 50:
            return '🚶'
        if rate < 200:
            return '🏃'
        if rate < 600:
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
        rate = VelocityIndicator._normalize_rate(burn_rate)
        if rate == 0:
            return 'idle'
        if rate < 10:
            return 'slow'
        if rate < 50:
            return 'moderate'
        if rate < 200:
            return 'fast'
        if rate < 600:
            return 'very fast'
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
        rate = VelocityIndicator._normalize_rate(burn_rate)
        emoji = VelocityIndicator.get_velocity_emoji(rate)
        rate_str = VelocityIndicator._format_rate(rate)
        if include_description:
            desc = VelocityIndicator.get_velocity_description(
                rate).capitalize()
            return f"{emoji} {desc} • {rate_str} tok/min"
        return f"{emoji} {rate_str} tok/min"
