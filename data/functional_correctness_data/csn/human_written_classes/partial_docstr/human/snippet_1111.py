from typing import Dict, List, Optional, Tuple
from collections import OrderedDict

class LocalesDict:

    def __init__(self):
        self.dict = OrderedDict()
        self._choice_cache = {}

    def list_locales(self) -> List[Optional[str]]:
        """
        Returns the list of available locales. The first locale is the default
        locale to be used. If no locales are known, then `None` will be the
        first item.
        """
        locales = list(self.dict.keys())
        if not locales:
            locales.append(None)
        return locales

    def choose_locale(self, locale: str) -> str:
        """
        Returns the best matching locale in what is available.

        :param locale: Locale to match
        :return: Locale to use
        """
        if locale not in self._choice_cache:
            locales = self.list_locales()
            best_choice = locales[0]
            best_level = 0
            for candidate in locales:
                cmp = compare_locales(locale, candidate)
                if cmp > best_level:
                    best_choice = candidate
                    best_level = cmp
            self._choice_cache[locale] = best_choice
        return self._choice_cache[locale]