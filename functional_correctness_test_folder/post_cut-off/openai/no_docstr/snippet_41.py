
class HeaderManager:
    """
    A simple helper that builds a list of HTTP‑style header strings.
    The headers include the requested plan, timezone, and a few
    generic headers that are useful for most APIs.
    """

    def __init__(self, plan: str = "pro", timezone: str = "Europe/Warsaw") -> None:
        """
        Initialise the manager with default plan and timezone values.
        These defaults can be overridden when calling :meth:`create_header`.
        """
        self.default_plan = plan
        self.default_timezone = timezone

    def create_header(
        self,
        plan: str | None = None,
        timezone: str | None = None,
    ) -> list[str]:
        """
        Build a list of header strings.

        Parameters
        ----------
        plan : str | None, optional
            The subscription plan to include in the headers.
            If ``None`` the default plan set in :meth:`__init__` is used.
        timezone : str | None, optional
            The timezone to include in the headers.
            If ``None`` the default timezone set in :meth:`__init__` is used.

        Returns
        -------
        list[str]
            A list of header strings ready to be used in an HTTP request.
        """
        # Resolve values, falling back to defaults if necessary
        plan = plan if plan is not None else self.default_plan
        timezone = timezone if timezone is not None else self.default_timezone

        # Construct the header list
        headers = [
            f"Plan: {plan}",
            f"Timezone: {timezone}",
            "User-Agent: HeaderManager/1.0",
            "Accept: application/json",
            "Content-Type: application/json",
        ]
        return headers
