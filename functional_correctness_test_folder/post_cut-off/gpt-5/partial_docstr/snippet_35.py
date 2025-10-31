from typing import List
from datetime import datetime, timezone as _timezone
from uuid import uuid4

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:  # pragma: no cover
    ZoneInfo = None  # Fallback handled in code


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        self._plans = {
            'free': {
                'label': 'Free',
                'support': 'Community forum support',
                'contact': 'https://support.example.com/community',
                'sla': 'No guaranteed SLA'
            },
            'pro': {
                'label': 'Pro',
                'support': 'Email support during business hours',
                'contact': 'support-pro@example.com',
                'sla': '8x5 support'
            },
            'enterprise': {
                'label': 'Enterprise',
                'support': 'Priority 24/7 support',
                'contact': 'support-enterprise@example.com',
                'sla': '24x7 support with SLA'
            }
        }
        self._default_plan_key = 'pro'
        self.last_incident_id: str | None = None

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        plan_key = (plan or '').strip().lower()
        plan_info = self._plans.get(
            plan_key, self._plans[self._default_plan_key])

        # Resolve timezone safely
        tz_label = timezone or 'UTC'
        dt: datetime
        if ZoneInfo is not None:
            try:
                dt = datetime.now(ZoneInfo(tz_label))
            except Exception:
                dt = datetime.now(_timezone.utc)
                tz_label = 'UTC'
        else:
            dt = datetime.now(_timezone.utc)
            tz_label = 'UTC'

        timestamp = dt.isoformat(timespec='seconds')
        incident_id = f"INC-{uuid4().hex[:8].upper()}"
        self.last_incident_id = incident_id

        lines: List[str] = []
        lines.append("=== Application Error ===")
        lines.append(f"Timestamp: {timestamp} ({tz_label})")
        lines.append(f"Incident ID: {incident_id}")
        lines.append("")
        lines.append("We're sorry, but something went wrong.")
        lines.append("")
        lines.append("What you can try:")
        lines.append("- Refresh the page.")
        lines.append("- Check your internet connection.")
        lines.append("- Clear browser cache and cookies.")
        lines.append("- Try again in a few minutes.")
        lines.append("")
        lines.append(f"Your plan: {plan_info['label']}")
        lines.append(f"Support: {plan_info['support']} ({plan_info['sla']})")
        lines.append(f"Contact: {plan_info['contact']}")
        lines.append("")
        lines.append(
            "If you contact support, include the Incident ID and timestamp.")
        return lines
