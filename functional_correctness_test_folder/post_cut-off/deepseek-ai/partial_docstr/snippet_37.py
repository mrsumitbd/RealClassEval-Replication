
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
            return "🐢"
        elif 1 <= burn_rate < 5:
            return "🚶"
        elif 5 <= burn_rate < 10:
            return "🏃"
        else:
            return "🚀"

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        if burn_rate < 1:
            return "Slow"
        elif 1 <= burn_rate < 5:
            return "Moderate"
        elif 5 <= burn_rate < 10:
            return "Fast"
        else:
            return "Very Fast"

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        emoji = VelocityIndicator.get_velocity_emoji(burn_rate)
        if include_description:
            description = VelocityIndicator.get_velocity_description(burn_rate)
            return f"{emoji} {description}"
        return emoji
