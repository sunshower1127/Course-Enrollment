from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Literal

from enhanced_selenium._utils.xpath_parser import get_xpath
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

if TYPE_CHECKING:
    from .driver import EnhancedChrome

axis_str = Literal[
    "ancestor",
    "ancestor-or-self",
    "child",
    "descendant",
    "descendant-or-self",
    "following",
    "following-sibling",
    "parent",
    "preceding",
    "preceding-sibling",
]


expr_str = str


# Interface for find, find_all
class Findable:
    # From other classes
    _driver: EnhancedChrome
    find_element: Callable[[str, str], WebElement]
    find_elements: Callable[[str, str], list[WebElement]]

    def find(
        self,
        xpath="",
        /,
        *,
        axis: axis_str = "descendant",
        tag="*",
        id: expr_str | None = None,
        id_contains: expr_str | None = None,
        name: expr_str | None = None,
        class_name: expr_str | None = None,
        class_name_contains: expr_str | None = None,
        text: expr_str | None = None,
        text_contains: expr_str | None = None,
        **kwargs: expr_str,
    ):
        xpath = xpath or get_xpath(locals())
        print(f"LOG: find: {xpath=}")
        try:
            return Element(
                self._driver._retry(lambda: self.find_element(By.XPATH, xpath))
            )
        except TimeoutException as e:
            if self._driver.debug:
                self._driver._debugfinder.find(xpath)
                return Element(
                    self._driver._retry(
                        lambda: self.find_element(By.XPATH, xpath)
                    )
                )
            else:
                msg = f"\n**Element not found**\n{xpath=}\n"
                raise TimeoutException(msg) from None

    def find_or_none(
        self,
        xpath="",
        /,
        *,
        axis: axis_str = "descendant",
        tag="*",
        id: expr_str | None = None,
        id_contains: expr_str | None = None,
        name: expr_str | None = None,
        class_name: expr_str | None = None,
        class_name_contains: expr_str | None = None,
        text: expr_str | None = None,
        text_contains: expr_str | None = None,
        **kwargs: expr_str,
    ):
        xpath = xpath or get_xpath(locals())

        try:
            return Element(self.find_element(By.XPATH, xpath))
        except (TimeoutException, NoSuchElementException):
            return None

    def find_all(
        self,
        xpath="",
        /,
        *,
        axis: axis_str = "descendant",
        tag="*",
        id: expr_str | None = None,
        id_contains: expr_str | None = None,
        name: expr_str | None = None,
        class_name: expr_str | None = None,
        class_name_contains: expr_str | None = None,
        text: expr_str | None = None,
        text_contains: expr_str | None = None,
        **kwargs: expr_str,
    ):
        xpath = xpath or get_xpath(locals())

        self.find(xpath)
        return Elements(
            [Element(e) for e in self.find_elements(By.XPATH, xpath)]
        )

    def find_all_or_none(
        self,
        xpath="",
        /,
        *,
        axis: axis_str = "descendant",
        tag="*",
        id: expr_str | None = None,
        id_contains: expr_str | None = None,
        name: expr_str | None = None,
        class_name: expr_str | None = None,
        class_name_contains: expr_str | None = None,
        text: expr_str | None = None,
        text_contains: expr_str | None = None,
        **kwargs: expr_str,
    ):
        xpath = xpath or get_xpath(locals())

        return Elements(
            [Element(e) for e in self.find_elements(By.XPATH, xpath)]
        )


# --------------------------------------------------------------------------------------


class Element(WebElement, Findable):
    def __init__(self, element: WebElement):
        super().__init__(element.parent, element.id)
        self._driver: EnhancedChrome = super().parent

    def up(self, levels=1):
        xpath = "/".join([".."] * levels)
        return Element(
            self._driver._retry(lambda: self.find_element(By.XPATH, xpath))
        )

    def move_mouse(self, offset_x=0, offset_y=0):
        ActionChains(self._parent).move_to_element_with_offset(
            self, offset_x, offset_y
        ).perform()
        return self

    def click(self, by: Literal["enter", "js", "mouse"] = "enter"):
        """
        기존 python_selenium이 지원하는 click 메서드는 가끔 클릭 안되는 에러가 있으니
        에러가 안나는 방향의 클릭들을 지원함.
        default = js
        """
        match by:
            case "enter":
                func = lambda: self.send_keys(Keys.ENTER)
            case "js":
                func = lambda: self._driver.execute_script(
                    "arguments[0].click();", self
                )
            case "mouse":
                func = lambda: ActionChains(self._parent).click(self).perform()

        self._driver._retry(func)

    def select(
        self,
        by: Literal["index", "value", "text"] = "index",
        value: str | int = 0,
    ):
        select = Select(self)
        match by:
            case "index":
                select.select_by_index(int(value))
            case "value":
                select.select_by_value(str(value))
            case "text":
                select.select_by_visible_text(str(value))


# --------------------------------------------------------------------------------------


class Elements:
    def __init__(self, elements: list[Element]):
        self._elements = elements
        self._index = 0
        self.texts = [element.text for element in self._elements]

    def __getitem__(self, index: int):
        return self._elements[index]

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._elements):
            result = self._elements[self._index]
            self._index += 1
            return result

        raise StopIteration

    def __bool__(self):
        return bool(self._elements)

    def up(self, levels=1):
        return Elements([element.up(levels) for element in self._elements])

    def find(
        self,
        xpath="",
        *,
        axis: axis_str = "descendant",
        tag="*",
        id: expr_str | None = None,
        id_contains: expr_str | None = None,
        name: expr_str | None = None,
        class_name: expr_str | None = None,
        class_name_contains: expr_str | None = None,
        text: expr_str | None = None,
        text_contains: expr_str | None = None,
        **kwargs: expr_str,
    ):
        xpath = xpath or get_xpath(locals())

        return Elements([element.find(xpath) for element in self._elements])

    def find_or_none(
        self,
        xpath="",
        *,
        axis: axis_str = "descendant",
        tag="*",
        id: expr_str | None = None,
        id_contains: expr_str | None = None,
        name: expr_str | None = None,
        class_name: expr_str | None = None,
        class_name_contains: expr_str | None = None,
        text: expr_str | None = None,
        text_contains: expr_str | None = None,
        **kwargs: expr_str,
    ):
        xpath = xpath or get_xpath(locals())

        result: list[Element] = []
        for element in self._elements:
            if (e := element.find_or_none(xpath)) is not None:
                result.append(e)
        return Elements(result)

    def click(self, by: Literal["default", "enter", "js", "mouse"] = "default"):
        match by:
            case "default":
                for element in self._elements:
                    element.click()

            case "enter":
                for element in self._elements:
                    element.send_keys(Keys.ENTER)

            case "js":
                self._elements[0]._driver.execute_script(
                    "arguments.forEach(e => e.click());", *self._elements
                )

            case "mouse":
                actions = ActionChains(self._elements[0]._driver)
                for element in self._elements:
                    actions.click(element)
                actions.perform()

    def send_keys(self, keys: str | list[str]):
        if isinstance(keys, str):
            for element in self._elements:
                element.send_keys(keys)

        else:
            for element, key in zip(self._elements, keys):
                element.send_keys(key)

    def attributes(
        self,
        name: str,
    ):
        return [element.get_attribute(name) for element in self._elements]
