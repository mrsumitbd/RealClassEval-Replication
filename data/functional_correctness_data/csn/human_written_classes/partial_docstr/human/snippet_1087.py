import functools
import logging.handlers

class SetupLogChecker:
    """A version of the LogChecker to use in classic TestCases."""

    def __init__(self, test_instance, log_path):
        self.handlers = [_StdlibStoringHandler(log_path)]
        if structlog is not None:
            sc = _StructlogCapturer()
            self.handlers.append(sc)
        self.test_instance = test_instance
        test_instance.assertLogged = functools.partial(self._check_pos, None)
        test_instance.assertLoggedCritical = functools.partial(self._check_pos, logging.CRITICAL)
        test_instance.assertLoggedError = functools.partial(self._check_pos, logging.ERROR)
        test_instance.assertLoggedWarning = functools.partial(self._check_pos, logging.WARNING)
        test_instance.assertLoggedInfo = functools.partial(self._check_pos, logging.INFO)
        test_instance.assertLoggedDebug = functools.partial(self._check_pos, logging.DEBUG)
        test_instance.assertNotLogged = functools.partial(self._check_neg, None)
        test_instance.assertNotLoggedCritical = functools.partial(self._check_neg, logging.CRITICAL)
        test_instance.assertNotLoggedError = functools.partial(self._check_neg, logging.ERROR)
        test_instance.assertNotLoggedWarning = functools.partial(self._check_neg, logging.WARNING)
        test_instance.assertNotLoggedInfo = functools.partial(self._check_neg, logging.INFO)
        test_instance.assertNotLoggedDebug = functools.partial(self._check_neg, logging.DEBUG)

    def _get_records(self):
        """Get the record objects from the logged data in all the handlers."""
        records = []
        for handler in self.handlers:
            records.extend(handler.records)
        return records

    def _check_pos(self, level, *tokens, **params):
        """Check if the different tokens were logged in one record, assert by level.

        The params are used for structlog information.
        """
        records = self._get_records()
        for record in records:
            record_match = all(((record.levelno == level or level is None) and token in record.message for token in tokens))
            if record_match:
                fields = record.extra_fields
                if all((fields.get(key, MISSING_MARK) == value for key, value in params.items())):
                    return
        level_name = logging.getLevelName(level)
        if params:
            repr_tokens = ', '.join(map(repr, tokens))
            params_data = ', '.join((f'{key}={value!r}' for key, value in params.items()))
            token_data = f'({repr_tokens}, {params_data})'
        else:
            token_data = repr(tokens)
        level_indicator = '' if level is None else f' in {level_name}'
        msgs = [f'Tokens {token_data} not found{level_indicator}, all was logged is...']
        for record in records:
            if record.extra_fields:
                fields_data = ', '.join((f'{key!r}: {value!r}' for key, value in record.extra_fields.items()))
                record_data = f'{record.message!r} {{{fields_data}}}'
            else:
                record_data = repr(record.message)
            msgs.append('    {:9s} {}'.format(record.levelname.upper(), record_data))
        self.test_instance.fail('\n'.join(msgs))

    def _check_neg(self, level, *tokens):
        """Check that the different tokens were NOT logged in one record, assert by level."""
        records = self._get_records()
        for record in records:
            if level is not None and record.levelno != level:
                continue
            if all((token in record.message for token in tokens)):
                break
        else:
            return
        msg = 'Tokens {} found in the following record:  {}  {!r}'.format(tokens, record.levelname, record.message)
        self.test_instance.fail(msg)