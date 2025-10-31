
class VelocityIndicator:

    @staticmethod
    def get_velocity_emoji(burn_rate: float) -> str:
        if burn_rate < 0.8:
            return "🐢"
        elif 0.8 <= burn_rate <= 1.2:
            return "🚀"
        else:
            return "🔥"

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        if burn_rate < 0.8:
            return "Below target velocity"
        elif 0.8 <= burn_rate <= 1.2:
            return "On target velocity"
        else:
            return "Above target velocity"

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        emoji = VelocityIndicator.get_velocity_emoji(burn_rate)
        if include_description:
            description = VelocityIndicator.get_velocity_description(burn_rate)
            return f"{emoji} {description}"
        return emoji
