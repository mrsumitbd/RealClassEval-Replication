import inspect

class BaseParam:
    """Base parameter class for subclassing.

    To create new parameter type subclass ``BaseParam`` and implement
    ``.value()`` method handler.

    Args:
        details (str): verbose description of parameter. Should contain all
            information that may be important to your API user and will be used
            for describing resource on ``OPTIONS`` requests and ``.describe()``
            call.

        label (str): human readable label for this parameter (it will be used
            for describing resource on OPTIONS requests).

            *Note that it is recomended to use parameter names that are
            self-explanatory intead of relying on param labels.*

        required (bool): if set to ``True`` then all GET, POST, PUT,
            PATCH and DELETE requests will return ``400 Bad Request`` response
            if query param is not provided. Defaults to ``False``.

        default (str): set default value for param if it is not
            provided in request as query parameter. This MUST be a raw string
            value that will be then parsed by ``.value()`` handler.

            If default is set and ``required`` is ``True`` it will raise
            ``ValueError`` as having required parameters with default
            value has no sense.

        many (str): set to ``True`` if multiple occurences of this parameter
            can be included in query string, as a result values for this
            parameter will be always included as a list in params dict.
            Defaults to ``False``. Instead of ``list`` you can use any
            list-compatible data type by overriding the ``container`` class
            attribute. See: :ref:`guide-params-custom-containers`.

            .. versionadded:: 0.1.0

        validators (list): list of validator callables.

            .. versionadded:: 0.2.0

    .. note::
        If ``many=False`` and client inlcudes multiple values for this
        parameter in query string then only one of those values will be
        returned, and it is undefined which one.

    **Example:**

    .. code-block:: python

           class BoolParam(BaseParam):
               def value(self, data):
                   if data in {'true', 'True', 'yes', '1', 'Y'}:
                       return True
                   elif data in {'false', 'False', 'no', '0', 'N'}:
                       return False
                   else:
                       raise ValueError(
                           "{data} is not valid boolean field".format(
                               data=data
                           )
                       )

    """
    spec = None
    type = None
    container = list

    def __init__(self, details, label=None, required=False, default=None, many=False, validators=None):
        """Initialize parameter and verify default/required contraints."""
        self.label = label
        self.details = details
        self.required = required
        self.many = many
        self.validators = validators or []
        if not default is None and (not isinstance(default, str)):
            raise TypeError("value for {cls} 'default' argument must be string instance".format(cls=self.__class__.__name__))
        if not default is None and required:
            raise ValueError("{cls}(required={required}, default='{default}'): initialization with both required and default makes no sense".format(cls=self.__class__.__name__, default=default, required=required))
        self.default = default

    def validated_value(self, raw_value):
        """Return parsed parameter value and run validation handlers.

        Error message included in exception will be included in http error
        response

        Args:
            value: raw parameter value to parse validate

        Returns:
            None

        Note:
            Concept of validation for params is understood here as a process
            of checking if data of valid type (successfully parsed/processed by
            ``.value()`` handler) does meet some other constraints
            (lenght, bounds, uniqueness, etc.). It will internally call its
            ``value()`` handler.

        """
        value = self.value(raw_value)
        try:
            for validator in self.validators:
                validator(value)
        except:
            raise
        else:
            return value

    def value(self, raw_value):
        """Raw value deserialization method handler.

        Args:
            raw_value (str): raw value from GET parameters

        """
        raise NotImplementedError('{cls}.value() method not implemented'.format(cls=self.__class__.__name__))

    def describe(self, **kwargs):
        """Describe this parameter instance for purpose of self-documentation.

        Args:
            kwargs (dict): dictionary of additional description items for
                extending default description

        Returns:
            dict: dictionary of description items


        Suggested way for overriding description fields or extending it with
        additional items is calling super class method with new/overriden
        fields passed as keyword arguments like following:

        .. code-block:: python

            class DummyParam(BaseParam):
                def description(self, **kwargs):
                    super().describe(is_dummy=True, **kwargs)

        """
        description = {'label': self.label, 'details': inspect.cleandoc(self.details), 'required': self.required, 'many': self.many, 'spec': self.spec, 'default': self.default, 'type': self.type or 'unspecified'}
        description.update(kwargs)
        return description