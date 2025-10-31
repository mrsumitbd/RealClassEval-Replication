
@step(retry_policy=ConstantDelayRetryPolicy(delay=5, maximum_attempts=10))
async def flaky(self, ev: StartEvent) -> StopEvent:
    ...
