from pypyr.errors import Call, ControlOfFlowInstruction, get_error_name, HandledError, LoopMaxExhaustedError, PipelineDefinitionError, Stop
from pypyr.utils import poll

class WhileDecorator:
    """While Decorator, as interpreted by the pypyr pipeline definition yaml.

    Encapsulate the methods that run a step in a while loop, and also maintains
    state necessary to run the loop. Given the need to maintain state, this is
    in a class, rather than purely functional code.

    In a normal world, Step invokes WhileDecorator. If you run it directly,
    you're responsible for the context and surrounding control-of-flow.

    External class consumers should probably use the while_loop method.
    while_loop serves as the blackbox entrypoint for this class' other methods.

    Attributes:
        error_on_max: (bool) defaults False. Raise error if max reached.
        max: (int) default None. Maximum loop iterations. None is infinite.
        sleep: (float) defaults 0. Sleep in seconds between iterations.
        stop:(bool) defaults None. Exit loop when stop is True.

    """

    def __init__(self, while_definition):
        """Initialize the class. No duh, huh.

        You can happily expect the initializer to initialize all
        member attributes.

        Args:
            while_definition: dict. This is the actual while definition as it
                              exists in the pipeline yaml.

        """
        logger.debug('starting')
        if isinstance(while_definition, dict):
            self.error_on_max = while_definition.get('errorOnMax', False)
            self.max = while_definition.get('max', None)
            self.sleep = while_definition.get('sleep', 0)
            self.stop = while_definition.get('stop', None)
            if self.stop is None and self.max is None:
                logger.error('while decorator missing both max and stop.')
                raise PipelineDefinitionError('the while decorator must have either max or stop, or both. But not neither. Note that setting stop: False with no max is an infinite loop. If an infinite loop is really what you want, set stop: False')
        else:
            logger.error('while decorator definition incorrect.')
            raise PipelineDefinitionError('while decorator must be a dict (i.e a map) type.')
        self.while_counter = None
        logger.debug('done')

    def exec_iteration(self, counter, context, step_method):
        """Run a single loop iteration.

        This method abides by the signature invoked by poll.while_until_true,
        which is to say (counter, *args, **kwargs). In a normal execution
        chain, this method's args passed by self.while_loop where context
        and step_method set. while_until_true injects counter as a 1st arg.

        Args:
            counter. int. loop counter, which number of iteration is this.
            context: (pypyr.context.Context) The pypyr context. This arg will
                     mutate - after method execution will contain the new
                     updated context.
            step_method: (method/function) This is the method/function that
                         will execute on every loop iteration. Signature is:
                         function(context)

         Returns:
            bool. True if self.stop evaluates to True after step execution,
                  False otherwise.

        """
        logger.debug('starting')
        context['whileCounter'] = counter
        self.while_counter = counter
        logger.info('while: running step with counter %s', counter)
        step_method(context)
        logger.debug('while: done step %s', counter)
        result = False
        if self.stop:
            result = context.get_formatted_as_type(self.stop, out_type=bool)
        logger.debug('done')
        return result

    def while_loop(self, context, step_method):
        """Run step inside a while loop.

        Args:
            context: (pypyr.context.Context) The pypyr context. This arg will
                     mutate - after method execution will contain the new
                     updated context.
            step_method: (method/function) This is the method/function that
                         will execute on every loop iteration. Signature is:
                         function(context)

        """
        logger.debug('starting')
        context['whileCounter'] = 0
        self.while_counter = 0
        if self.stop is None and self.max is None:
            logger.error('while decorator missing both max and stop.')
            raise PipelineDefinitionError('the while decorator must have either max or stop, or both. But not neither.')
        error_on_max = context.get_formatted_as_type(self.error_on_max, out_type=bool)
        sleep = context.get_formatted_as_type(self.sleep, out_type=float)
        if self.max is None:
            max = None
            logger.info('while decorator will loop until %s evaluates to True at %ss intervals.', self.stop, sleep)
        else:
            max = context.get_formatted_as_type(self.max, out_type=int)
            if max < 1:
                logger.info('max %s is %s. while only runs when max > 0.', self.max, max)
                logger.debug('done')
                return
            if self.stop is None:
                logger.info('while decorator will loop %s times at %ss intervals.', max, sleep)
            else:
                logger.info('while decorator will loop %s times, or until %s evaluates to True at %ss intervals.', max, self.stop, sleep)
        if not poll.while_until_true(interval=sleep, max_attempts=max)(self.exec_iteration)(context=context, step_method=step_method):
            if error_on_max:
                logger.error('exhausted %s iterations of while loop, and errorOnMax is True.', max)
                if self.stop and max:
                    raise LoopMaxExhaustedError(f'while loop reached {max} and {self.stop} never evaluated to True.')
                else:
                    raise LoopMaxExhaustedError(f'while loop reached {max}.')
            elif self.stop and max:
                logger.info('while decorator looped %s times, and %s never evaluated to True.', max, self.stop)
            logger.debug('while loop done')
        else:
            logger.info('while loop done, stop condition %s evaluated True.', self.stop)
        logger.debug('done')