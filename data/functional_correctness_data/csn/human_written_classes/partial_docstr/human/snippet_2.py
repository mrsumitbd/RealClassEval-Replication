from typing import Literal, Optional

class By:
    """Set of supported locator strategies.

    ID:
    --
    Select the element by its ID.

    >>> element = driver.find_element(By.ID, "myElement")

    XPATH:
    ------
    Select the element via XPATH.
        - absolute path
        - relative path

    >>> element = driver.find_element(By.XPATH, "//html/body/div")

    LINK_TEXT:
    ----------
    Select the link element having the exact text.

    >>> element = driver.find_element(By.LINK_TEXT, "myLink")

    PARTIAL_LINK_TEXT:
    ------------------
    Select the link element having the partial text.

    >>> element = driver.find_element(By.PARTIAL_LINK_TEXT, "my")

    NAME:
    ----
    Select the element by its name attribute.

    >>> element = driver.find_element(By.NAME, "myElement")

    TAG_NAME:
    --------
    Select the element by its tag name.

    >>> element = driver.find_element(By.TAG_NAME, "div")

    CLASS_NAME:
    -----------
    Select the element by its class name.

    >>> element = driver.find_element(By.CLASS_NAME, "myElement")

    CSS_SELECTOR:
    -------------
    Select the element by its CSS selector.

    >>> element = driver.find_element(By.CSS_SELECTOR, "div.myElement")
    """
    ID = 'id'
    XPATH = 'xpath'
    LINK_TEXT = 'link text'
    PARTIAL_LINK_TEXT = 'partial link text'
    NAME = 'name'
    TAG_NAME = 'tag name'
    CLASS_NAME = 'class name'
    CSS_SELECTOR = 'css selector'
    _custom_finders: dict[str, str] = {}

    @classmethod
    def register_custom_finder(cls, name: str, strategy: str) -> None:
        cls._custom_finders[name] = strategy

    @classmethod
    def get_finder(cls, name: str) -> Optional[str]:
        return cls._custom_finders.get(name) or getattr(cls, name.upper(), None)

    @classmethod
    def clear_custom_finders(cls) -> None:
        cls._custom_finders.clear()