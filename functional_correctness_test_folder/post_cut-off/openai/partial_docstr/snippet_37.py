
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
        # Ensure burn_rate is non‑negative
        rate = max(0.0, burn_rate)

        if rate < 10:
            return "🐢"   # Slow
        if rate < 30:
            return "🐇"   # Moderate
        if rate < 60:
            return "🚀"   # Fast
        return "⚡"       # Super fast

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        '''Get textual description of velocity based on burn rate.
        Args:
            burn_rate: Token burn rate per minute
        Returns:
            Human‑readable description of velocity level
        '''
        rate = max(0.0, burn_rate)

        if rate < 10:
            return "Slow burn"
        if rate < 30:
            return "Moderate burn"
        if rate < 60:
            return "Fast burn"
        return "Super fast burn"

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        '''Render the velocity indicator.
        Args:
            burn_rate: Token burn rate per minute
            include_description: If True, append the description after the emoji
        Returns:
            A string containing the emoji (and optionally the description)
        '''
        emoji = VelocityIndicator.get_velocity_emoji(burn_rate)
        if include_description:
            description = VelocityIndicator.get_velocity_description(burn_rate)
            return f"{emoji} {description}"
        return emoji
