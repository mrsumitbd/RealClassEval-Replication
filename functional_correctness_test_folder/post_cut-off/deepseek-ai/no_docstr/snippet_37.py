
class VelocityIndicator:

    @staticmethod
    def get_velocity_emoji(burn_rate: float) -> str:
        if burn_rate < 0.5:
            return "🐢"
        elif 0.5 <= burn_rate < 1.0:
            return "🚶"
        elif 1.0 <= burn_rate < 1.5:
            return "🏃"
        else:
            return "🚀"

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        if burn_rate < 0.5:
            return "Very slow"
        elif 0.5 <= burn_rate < 1.0:
            return "Slow"
        elif 1.0 <= burn_rate < 1.5:
            return "Fast"
        else:
            return "Very fast"

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        emoji = VelocityIndicator.get_velocity_emoji(burn_rate)
        if include_description:
            description = VelocityIndicator.get_velocity_description(burn_rate)
            return f"{emoji} {description}"
        else:
            return emoji
