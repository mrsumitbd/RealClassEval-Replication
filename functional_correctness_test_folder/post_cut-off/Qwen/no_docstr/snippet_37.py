
class VelocityIndicator:

    @staticmethod
    def get_velocity_emoji(burn_rate: float) -> str:
        if burn_rate < 0.5:
            return "🐢"
        elif 0.5 <= burn_rate < 1.5:
            return "🚶‍♂️"
        elif 1.5 <= burn_rate < 2.5:
            return "🏃‍♂️"
        else:
            return "💨"

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        if burn_rate < 0.5:
            return "Very Slow"
        elif 0.5 <= burn_rate < 1.5:
            return "Moderate"
        elif 1.5 <= burn_rate < 2.5:
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
