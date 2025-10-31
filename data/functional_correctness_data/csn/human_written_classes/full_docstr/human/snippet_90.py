from pypyr.utils import poll
from pypyr.errors import Call, ControlOfFlowInstruction, get_error_name, HandledError, LoopMaxExhaustedError, PipelineDefinitionError, Stop
from pypyr.cache.backoffcache import backoff_cache
from pypyr.config import config

class RetryDecorator:
    """Retry decorator, as interpreted by the pypyr pipeline definition yaml.

    Encapsulate the methods that run a step in a retry loop, and also maintains
    state necessary to run the loop. Given the need to maintain state, this is
    in a class, rather than purely functional code.

    In a normal world, Step invokes RetryDecorator. If you run it directly,
    you're responsible for the context and surrounding control-of-flow.

    External class consumers should probably use the retry_loop method.
    retry_loop serves as the blackbox entrypoint for this class' other methods.

    Attributes:
        backoff (str): default 'fixed'. Absolute name of back-off strategy.
            Builtin strategies allow aliases like fixed, linear, jitter. Custom
            backoff should give absolute name to callable derived from
            pypyr.retries.BackoffBase.
        backoff_args (any): User provided arguments for back-off strategy.
            Likely want to use a dict here.
        jrc (float): default 0. Jitter Range Coefficient. Jitter finds a random
            value between (jrc*sleep) and (sleep).
        max (int):  default None. Maximum loop iterations. None is infinite.
        sleep (float or list[float]):  defaults 0. Sleep in seconds between
            iterations.
        sleep_max (float): default None. Maximum value for sleep if using a
            backoff strategy that calculates sleep interval. None means sleep
            can increase indefinitely.
        stop_on (list[str]): default None. Always stop retry on these error
            types. None means retry on all errors.
        retry_on (list[str]): default None. Only retry on these error types.
            All other error types will stop retry loop. None means retry all
            errors.

    """

    def __init__(self, retry_definition):
        """Initialize the class. No duh, huh.

        You can happily expect the initializer to initialize all
        member attributes.

        Args:
            retry_definition: dict. This is the actual retry definition as it
                              exists in the pipeline yaml.

        """
        logger.debug('starting')
        if isinstance(retry_definition, dict):
            self.backoff = retry_definition.get('backoff', None)
            self.backoff_args = retry_definition.get('backoffArgs', None)
            self.jrc = retry_definition.get('jrc', 0)
            self.max = retry_definition.get('max', None)
            self.sleep = retry_definition.get('sleep', 0)
            self.sleep_max = retry_definition.get('sleepMax', None)
            self.stop_on = retry_definition.get('stopOn', None)
            self.retry_on = retry_definition.get('retryOn', None)
        else:
            logger.error('retry decorator definition incorrect.')
            raise PipelineDefinitionError('retry decorator must be a dict (i.e a map) type.')
        self.retry_counter = None
        logger.debug('done')

    def exec_iteration(self, counter, context, step_method, max):
        """Run a single retry iteration.

        This method abides by the signature invoked by poll.while_until_true,
        which is to say (counter, *args, **kwargs). In a normal execution
        chain, this method's args passed by self.retry_loop where context
        and step_method set. while_until_true injects counter as a 1st arg.

        Args:
            counter. int. loop counter, which number of iteration is this.
            context: (pypyr.context.Context) The pypyr context. This arg will
                     mutate - after method execution will contain the new
                     updated context.
            step_method: (method/function) This is the method/function that
                         will execute on every loop iteration. Signature is:
                         function(context)
            max: int. Execute step_method function up to this limit

         Returns:
            bool. True if step execution completed without error.
                  False if error occured during step execution.

        """
        logger.debug('starting')
        context['retryCounter'] = counter
        self.retry_counter = counter
        logger.info('retry: running step with counter %s', counter)
        try:
            step_method(context)
            result = True
        except (ControlOfFlowInstruction, Stop):
            raise
        except Exception as ex_info:
            if max:
                if counter == max:
                    logger.debug('retry: max %s retries exhausted. raising error.', counter)
                    raise
            if isinstance(ex_info, HandledError):
                ex_info = ex_info.__cause__
            if self.stop_on or self.retry_on:
                error_name = get_error_name(ex_info)
                if self.stop_on:
                    formatted_stop_list = context.get_formatted_value(self.stop_on)
                    if error_name in formatted_stop_list:
                        logger.error('%s in stopOn. Raising error and exiting retry.', error_name)
                        raise
                    else:
                        logger.debug('%s not in stopOn. Continue.', error_name)
                if self.retry_on:
                    formatted_retry_list = context.get_formatted_value(self.retry_on)
                    if error_name not in formatted_retry_list:
                        logger.error('%s not in retryOn. Raising error and exiting retry.', error_name)
                        raise
                    else:
                        logger.debug('%s in retryOn. Retry again.', error_name)
            result = False
            logger.error('retry: ignoring error because retryCounter < max.\n%s: %s', type(ex_info).__name__, ex_info)
        logger.debug('retry: done step with counter %s', counter)
        logger.debug('done')
        return result

    def retry_loop(self, context, step_method):
        """Run step inside a retry loop.

        Args:
            context: (pypyr.context.Context) The pypyr context. This arg will
                     mutate - after method execution will contain the new
                     updated context.
            step_method: (method/function) This is the method/function that
                         will execute on every loop iteration. Signature is:
                         function(context)

        """
        logger.debug('starting')
        context['retryCounter'] = 0
        self.retry_counter = 0
        sleep = context.get_formatted_value(self.sleep)
        backoff_name = context.get_formatted_value(self.backoff) if self.backoff else config.default_backoff
        max_sleep = None
        if self.sleep_max:
            max_sleep = context.get_formatted_as_type(self.sleep_max, out_type=float)
        jrc = context.get_formatted_value(self.jrc)
        backoff_args = context.get_formatted_value(self.backoff_args)
        backoff_callable = backoff_cache.get_backoff(backoff_name)(sleep=sleep, max_sleep=max_sleep, jrc=jrc, kwargs=backoff_args)
        if self.max:
            max = context.get_formatted_as_type(self.max, out_type=int)
            logger.info('retry decorator will try %d times with %s backoff starting at %ss intervals.', max, backoff_name, sleep)
        else:
            max = None
            logger.info('retry decorator will try indefinitely with %s backoff starting at %ss intervals.', backoff_name, sleep)
        is_retry_ok = poll.while_until_true(interval=backoff_callable, max_attempts=max)(self.exec_iteration)(context=context, step_method=step_method, max=max)
        assert is_retry_ok
        logger.debug('retry loop complete, reporting success.')
        logger.debug('done')