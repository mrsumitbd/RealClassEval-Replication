
class VelocityIndicator:

    @staticmethod
    def get_velocity_emoji(burn_rate: float) -> str:
        if burn_rate < 0.1:
            return "🐌"
        elif burn_rate < 0.2:
            return "🐢"
        elif burn_rate < 0.3:
            return "🐇"
        elif burn_rate < 0.4:
            return "🐎"
        elif burn_rate < 0.5:
            return "🏇"
        elif burn_rate < 0.6:
            return "🏁"
        elif burn_rate < 0.7:
            return "🚀"
        elif burn_rate < 0.8:
            return "🌌"
        elif burn_rate < 0.9:
            return "🌠"
        else:
            return "💫"

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        if burn_rate < 0.1:
            return "Very Slow"
        elif burn_rate < 0.2:
            return "Slow"
        elif burn_rate < 0.3:
            return "Moderate"
        elif burn_rate < 0.4:
            return "Fast"
        elif burn_rate < 0.5:
            return "Very Fast"
        elif burn_rate < 0.6:
            return "Blazing"
        elif burn_rate < 0.7:
            return "Speedy"
        elif burn_rate < 0.8:
            return "Turbo"
        elif burn_rate < 0.9:
            return "Hyper"
        else:
            return "Ludicrous"

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        emoji = VelocityIndicator.get_velocity_emoji(burn_rate)
        if include_description:
            description = VelocityIndicator.get_velocity_description(burn_rate)
            return f"{emoji} {description}"
        return emoji
