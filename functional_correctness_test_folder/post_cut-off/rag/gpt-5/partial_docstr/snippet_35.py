from typing import List
from datetime import datetime, timezone as dt_timezone

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        self._timestamp_format = '%Y-%m-%d %H:%M:%S %Z'
        self._header = 'Error: Failed to fetch data'
        self._subheader = 'We could not load your data at this time.'
        self._support_email = 'support@example.com'
        self._status_url = 'https://status.example.com'
        self._docs_url = 'https://docs.example.com/troubleshooting#data-loading'
        self._upgrade_url = 'https://app.example.com/upgrade'
        self._plan_advice = {
            'free': [
                '- You may have reached the free tier rate limit.',
                f'- Consider upgrading for higher limits: {self._upgrade_url}',
            ],
            'trial': [
                '- You may have reached trial limits.',
                f'- Consider upgrading to continue without interruption: {self._upgrade_url}',
            ],
            'pro': [
                '- Verify API credentials and data source permissions.',
                '- Check if your workspace has access to this dataset.',
            ],
            'team': [
                '- Verify role-based access controls for your team.',
                '- Ensure the dataset is shared with your team or project.',
            ],
            'enterprise': [
                '- Check organization-level network rules or SSO status.',
                '- Reach out to your Customer Success Manager if needed.',
            ],
        }

    def _now_in_timezone(self, tz_name: str) -> (datetime, bool):
        fallback_used = False
        if ZoneInfo is not None:
            try:
                tzinfo = ZoneInfo(tz_name)
            except Exception:
                tzinfo = dt_timezone.utc
                fallback_used = True
        else:
            tzinfo = dt_timezone.utc
            fallback_used = (tz_name.upper() != 'UTC')
        return datetime.now(tzinfo), fallback_used

    def _normalize_plan(self, plan: str) -> str:
        if not isinstance(plan, str) or not plan:
            return 'unknown'
        p = plan.strip().lower()
        aliases = {
            'professional': 'pro',
            'basic': 'free',
            'community': 'free',
            'enterprise-plus': 'enterprise',
            'team-plus': 'team',
        }
        return aliases.get(p, p)

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        '''Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        '''
        normalized_plan = self._normalize_plan(plan)
        now, used_fallback_tz = self._now_in_timezone(timezone)
        human_plan = normalized_plan.capitalize(
        ) if normalized_plan != 'unknown' else 'Unknown'

        lines: List[str] = []
        lines.append(self._header)
        lines.append(self._subheader)
        lines.append(f'Time: {now.strftime(self._timestamp_format)}')
        lines.append(f'Plan: {human_plan}')
        if used_fallback_tz:
            lines.append(
                f'Note: Unrecognized timezone "{timezone}". Showing times in UTC.')

        lines.append('What you can try:')
        lines.append(
            '- Retry the action (Ctrl/Cmd + R) or try again in a moment.')
        lines.append(
            '- Check your internet connection and VPN/proxy settings.')
        lines.append(
            '- Verify that the data source or API endpoint is reachable.')
        lines.append('- If you recently changed credentials, re-authenticate.')

        if normalized_plan in self._plan_advice:
            lines.extend(self._plan_advice[normalized_plan])
        else:
            lines.append(
                '- Verify your account permissions for this resource.')

        lines.append('If the problem persists:')
        lines.append(f'- Check system status: {self._status_url}')
        lines.append(f'- Troubleshooting guide: {self._docs_url}')
        lines.append(f'- Contact support: {self._support_email}')

        return lines
