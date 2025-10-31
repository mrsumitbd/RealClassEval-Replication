class Retrying:

    def __init__(self, policies, before_retry):
        """
        Parameters
        ----------
        policies: list[qiniu.retry.abc.RetryPolicy]
        before_retry: callable
            `(attempt: Attempt, policy: qiniu.retry.abc.RetryPolicy) -> bool`
        """
        self.policies = policies
        self.before_retry = before_retry
        self.context = {}

    def init_context(self):
        for policy in self.policies:
            policy.init_context(self.context)

    def get_retry_policy(self, attempt):
        """

        Parameters
        ----------
        attempt: Attempt

        Returns
        -------
        qiniu.retry.abc.RetryPolicy

        """
        policy = None
        for p in self.policies:
            if p.is_important(attempt):
                policy = p
                break
        if policy and policy.should_retry(attempt):
            return policy
        else:
            policy = None
        for p in self.policies:
            if p.should_retry(attempt):
                policy = p
                break
        return policy

    def after_retried(self, attempt, policy):
        for p in self.policies:
            p.after_retry(attempt, policy)