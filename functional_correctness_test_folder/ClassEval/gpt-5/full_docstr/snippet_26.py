class CookiesUtil:
    """
    This is a class as utility for managing and manipulating Cookies, including methods for retrieving, saving, and setting Cookies data.
    """

    def __init__(self, cookies_file):
        """
        Initializes the CookiesUtil with the specified cookies file.
        :param cookies_file: The cookies file to use, str.
        """
        self.cookies_file = cookies_file
        self.cookies = None

    def get_cookies(self, reponse):
        """
        Gets the cookies from the specified response,and save it to cookies_file.
        :param reponse: The response to get cookies from, dict.
        >>> cookies_util = CookiesUtil('cookies.json')
        >>> cookies_util.get_cookies({'cookies': {'key1': 'value1', 'key2': 'value2'}})
        >>> cookies_util.cookies
        {'key1': 'value1', 'key2': 'value2'}

        """
        cookies = {}
        # Try dict input
        if isinstance(reponse, dict) and 'cookies' in reponse:
            value = reponse.get('cookies', {})
            if isinstance(value, dict):
                cookies = value
            else:
                try:
                    cookies = dict(value)
                except Exception:
                    cookies = {}
        # Try object with .cookies attribute (e.g., requests.Response)
        elif hasattr(reponse, 'cookies'):
            rc = getattr(reponse, 'cookies')
            try:
                if isinstance(rc, dict):
                    cookies = rc
                elif hasattr(rc, 'items'):
                    cookies = {k: v for k, v in rc.items()}
                else:
                    cookies = dict(rc)
            except Exception:
                cookies = {}
        self.cookies = cookies
        self._save_cookies()
        return cookies

    def load_cookies(self):
        """
        Loads the cookies from the cookies_file to the cookies data.
        :return: The cookies data, dict.
        >>> cookies_util = CookiesUtil('cookies.json')
        >>> cookies_util.load_cookies()
        {'key1': 'value1', 'key2': 'value2'}

        """
        import json
        import os

        if not isinstance(self.cookies_file, str) or not self.cookies_file:
            self.cookies = {}
            return self.cookies

        if not os.path.exists(self.cookies_file):
            self.cookies = {}
            return self.cookies

        try:
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.cookies = data
                else:
                    # Ensure dict type
                    try:
                        self.cookies = dict(data)
                    except Exception:
                        self.cookies = {}
        except Exception:
            self.cookies = {}
        return self.cookies

    def _save_cookies(self):
        """
        Saves the cookies to the cookies_file, and returns True if successful, False otherwise.
        :return: True if successful, False otherwise.
        >>> cookies_util = CookiesUtil('cookies.json')
        >>> cookies_util.cookies = {'key1': 'value1', 'key2': 'value2'}
        >>> cookies_util._save_cookies()
        True

        """
        import json
        import os

        try:
            data = self.cookies
            if data is None:
                data = {}
            elif not isinstance(data, dict):
                try:
                    data = dict(data)
                except Exception:
                    return False

            dirname = os.path.dirname(os.path.abspath(self.cookies_file))
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname, exist_ok=True)

            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, sort_keys=True)
            return True
        except Exception:
            return False
