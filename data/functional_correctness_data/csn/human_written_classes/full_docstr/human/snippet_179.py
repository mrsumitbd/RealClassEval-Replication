from typing import Any, Optional
from functools import cached_property

class GetHeaders:
    """Mixin to get a header"""

    def get_header_value(self, name: str) -> Optional[str]:
        """
        Returns the header value of the header defined in ``name``

        :param name: Name of the header to get the value of
        :type name: str
        :return: Value of the header
        :rtype: Optional[str]
        """
        for header in self.raw_entry['headers']:
            if header['name'].lower() == name.lower():
                return header['value']
        return None

    @cached_property
    def _formatted_headers(self) -> str:
        """
        Returns a formatted string of the headers in `KEY: VALUE` format

        :return: string of all headers
        :rtype: str
        """
        formatted_headers = ''
        for header in self.raw_entry['headers']:
            name, value = (header['name'], header['value'])
            formatted_headers += f'{name}: {value}\n'
        return formatted_headers