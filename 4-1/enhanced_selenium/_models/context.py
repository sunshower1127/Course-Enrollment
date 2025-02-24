# from typing import TYPE_CHECKING

from selenium.common.exceptions import NoSuchElementException, TimeoutException

# if TYPE_CHECKING:
#     from models.core.driver import ChromeDriver


class _NoError:
    def __init__(self, driver):
        self.driver = driver
        self.debug = self.driver.debug

    def __enter__(self):
        if self.debug:
            self.driver.debug = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.debug:
            self.driver.debug = True
        return True


class _RepeatSetting:
    def __init__(self, driver, timeout=None, freq=None):
        self.driver = driver
        self.orig_timeout = self.driver._timeout
        self.orig_freq = self.driver._freq

        self.timeout = timeout or self.orig_timeout
        self.freq = freq or self.orig_freq

    def __enter__(self):
        self.driver._timeout = self.timeout
        self.driver._freq = self.freq
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver._timeout = self.orig_timeout
        self.driver._freq = self.orig_freq
        return False  # 예외를 억제하지 않음
