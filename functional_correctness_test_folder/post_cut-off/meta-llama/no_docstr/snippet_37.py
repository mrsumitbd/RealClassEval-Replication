
class VelocityIndicator:

    @staticmethod
    def get_velocity_emoji(burn_rate: float) -> str:
        if burn_rate < 0.5:
            return "⬇️"
        elif burn_rate < 1.0:
            return "😐"
        elif burn_rate < 1.5:
            return "⬆️"
        else:
            return "⚡️"

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        if burn_rate < 0.5:
            return "Very Low"
        elif burn_rate < 1.0:
            return "Low"
        elif burn_rate < 1.5:
            return "Moderate"
        else:
            return "High"

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        emoji = VelocityIndicator.get_velocity_emoji(burn_rate)
        if include_description:
            description = VelocityIndicator.get_velocity_description(burn_rate)
            return f"{emoji} {description} ({burn_rate:.2f})"
        else:
            return f"{emoji} ({burn_rate:.2f})"
