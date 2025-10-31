class VelocityIndicator:
    '''Velocity indicator component for burn rate visualization.'''

    @staticmethod
    def _normalize_burn_rate(burn_rate: float) -> float:
        try:
            br = float(burn_rate)
        except (TypeError, ValueError):
            return 0.0
        if br != br:  # NaN check
            return 0.0
        return br

    @staticmethod
    def get_velocity_emoji(burn_rate: float) -> str:
        '''Get velocity emoji based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Emoji representing velocity level
        '''
        br = VelocityIndicator._normalize_burn_rate(burn_rate)
        if br <= 0:
            return "🛑"
        if br < 50:
            return "🐢"
        if br < 200:
            return "🚶"
        if br < 600:
            return "🏃"
        if br < 1500:
            return "🚀"
        return "☄️"

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        br = VelocityIndicator._normalize_burn_rate(burn_rate)
        if br <= 0:
            return "No burn"
        if br < 50:
            return "Very low burn"
        if br < 200:
            return "Low burn"
        if br < 600:
            return "Moderate burn"
        if br < 1500:
            return "High burn"
        return "Extreme burn"

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        br = VelocityIndicator._normalize_burn_rate(burn_rate)
        emoji = VelocityIndicator.get_velocity_emoji(br)
        if not include_description:
            return emoji
        desc = VelocityIndicator.get_velocity_description(br)
        return f"{emoji} {desc}"
