class DictTransformer:
    """`@property _dict` can overridden"""

    @property
    def _dict(self):
        return self.__dict__

    def str_format(self, format_: str) -> str:
        """From instance to str with formatting

        :param format_: format string
        :return: str

        Usage:

            >>> from owlmixin.samples import Human, Food
            >>> human_dict = {
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "favorites": [
            ...         {"name": "Apple", "names_by_lang": {"en": "Apple"}}
            ...     ]
            ... }
            >>> Human.from_dict(human_dict).str_format('{id}: {name}')
            '1: Tom'
        """
        return format_.format(**self.to_dict())

    def to_dict(self, *, ignore_none: bool=True, force_value: bool=True, ignore_empty: bool=False) -> dict:
        """From instance to dict

        :param ignore_none: Properties which is None are excluded if True
        :param force_value: Transform to value using to_value (default: str()) of ValueTransformer which inherited if True
        :param ignore_empty: Properties which is empty are excluded if True
        :return: Dict

        Usage:
            >>> from owlmixin.samples import Human, Food
            >>> human_dict = {
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "favorites": [
            ...         {"name": "Apple", "names_by_lang": {"en": "Apple"}}
            ...     ]
            ... }
            >>> Human.from_dict(human_dict).to_dict() == human_dict
            True

        You can include None properties by specifying False for ignore_none

            >>> f = Food.from_dict({"name": "Apple"}).to_dict(ignore_none=False)
            >>> f["name"]
            'Apple'
            >>> "names_by_lang" in f
            True
            >>> f["names_by_lang"]

        As default

            >>> f = Food.from_dict({"name": "Apple"}).to_dict()
            >>> f["name"]
            'Apple'
            >>> "names_by_lang" in f
            False

        You can exclude Empty properties by specifying True for ignore_empty

            >>> f = Human.from_dict({"id": 1, "name": "Ichiro", "favorites": []}).to_dict()
            >>> f["favorites"]
            []
            >>> f = Human.from_dict({"id": 1, "name": "Ichiro", "favorites": []}).to_dict(ignore_empty=True)
            >>> "favorites" in f
            False

        """
        return traverse_dict(self._dict, ignore_none, force_value, ignore_empty)