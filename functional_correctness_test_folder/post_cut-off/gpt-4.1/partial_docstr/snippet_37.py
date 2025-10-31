
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
        if burn_rate < 1:
            return "🐢"  # Turtle for very slow
        elif burn_rate < 5:
            return "🚶"  # Walking person for slow
        elif burn_rate < 20:
            return "🏃"  # Running person for moderate
        elif burn_rate < 50:
            return "🚗"  # Car for fast
        elif burn_rate < 100:
            return "🚀"  # Rocket for very fast
        else:
            return "💥"  # Explosion for extreme

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        if burn_rate < 1:
            return "Very slow"
        elif burn_rate < 5:
            return "Slow"
        elif burn_rate < 20:
            return "Moderate"
        elif burn_rate < 50:
            return "Fast"
        elif burn_rate < 100:
            return "Very fast"
        else:
            return "Extreme"

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        emoji = VelocityIndicator.get_velocity_emoji(burn_rate)
        if include_description:
            desc = VelocityIndicator.get_velocity_description(burn_rate)
            return f"{emoji} {desc} ({burn_rate:.2f}/min)"
        else:
            return f"{emoji} {burn_rate:.2f}/min"
