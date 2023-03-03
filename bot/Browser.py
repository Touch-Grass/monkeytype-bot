from typing import Union

from playwright.async_api import async_playwright, Browser as PWBrowser, Playwright, Page

from models.metaclasses.singleton import SingletonMeta


class Browser(metaclass=SingletonMeta):
    """
    A wrapper around Playwright's browser object.
    """

    def __init__(self, timeout: int = 1000):
        self._playwright: Union[Playwright, None] = None
        self._browser: Union[PWBrowser, None] = None
        self._page: Union[Page, None] = None

        self.timeout = timeout

    async def initialize(self) -> None:
        """
        Initializes the browser and navigates to MonkeyType.
        """
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.firefox.launch(headless=False, timeout=self.timeout)

        self._page = await self._browser.new_page()
        await self._page.goto("https://monkeytype.com")

    async def close(self) -> None:
        """
        Closes the browser and stops Playwright.
        """
        await self._browser.close()
        self._playwright.stop()

    @property
    def browser(self) -> PWBrowser:
        return self._browser

    @property
    def playwright(self) -> Playwright:
        return self._playwright

    @property
    def page(self) -> Page:
        return self._page
