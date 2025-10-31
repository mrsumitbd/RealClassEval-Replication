class VelocityIndicator:

    @staticmethod
    def get_velocity_emoji(burn_rate: float) -> str:
        try:
            import math
            if burn_rate is None or not math.isfinite(burn_rate):
                return "❓"
            if burn_rate < 0:
                return "❓"
            if burn_rate < 0.5:
                return "🟢"
            if burn_rate < 1.0:
                return "🟡"
            if burn_rate < 1.5:
                return "🟠"
            return "🔴"
        except Exception:
            return "❓"

    @staticmethod
    def get_velocity_description(burn_rate: float) -> str:
        try:
            import math
            if burn_rate is None or not math.isfinite(burn_rate):
                return "Unknown burn rate"
            if burn_rate < 0:
                return "Invalid (negative) burn rate"
            if burn_rate < 0.5:
                return "Healthy burn rate"
            if burn_rate < 1.0:
                return "Cautionary burn rate"
            if burn_rate < 1.5:
                return "High burn rate"
            return "Critical burn rate"
        except Exception:
            return "Unknown burn rate"

    @staticmethod
    def render(burn_rate: float, include_description: bool = False) -> str:
        emoji = VelocityIndicator.get_velocity_emoji(burn_rate)
        if not include_description:
            return emoji
        desc = VelocityIndicator.get_velocity_description(burn_rate)
        return f"{emoji} {desc}"
