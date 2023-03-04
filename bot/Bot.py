import random
import time
from typing import List

import pyautogui
from playwright.async_api import ElementHandle

from bot.Browser import Browser


class Bot:
    def __init__(self):
        self.browser = Browser()

    async def init(self, username: str, password: str) -> None:
        await self.browser.initialize()
        await self._accept_cookies_then_sign_in(username, password)

    async def get_prompt(self) -> str:
        import string

        words: List[ElementHandle] = await (await self.browser.page.query_selector("#words")).query_selector_all(
            ".word")
        sentence: List[str] = []

        for i in range(len(words)):
            word = await words[i].text_content()
            if random.random() < 0.05:
                index = random.randrange(len(word))
                new_char = string.ascii_letters[random.randint(0, 25)]
                if i + 1 < len(words):
                    word = word[:index] + new_char + word[index + 1:]
            sentence.append(word)

        return ' '.join(sentence)

    async def _choose_mode(self) -> None:
        try:
            await (await self.browser.page.wait_for_selector(".textButton[mode='words']", timeout=1000)).click()

        except TimeoutError as err:
            print(f"Error: {err}")

    async def _accept_cookies_then_sign_in(self, username: str, password: str) -> None:
        try:
            await (await self.browser.page.wait_for_selector(".acceptAll", timeout=5000)).click()

        except TimeoutError as err:
            print(f"Error accepting all cookies: {err}")

        finally:
            await self._sign_in(username, password)

    async def _sign_in(self, username: str, password: str) -> None:
        print("Signing in...")
        try:
            await (await self.browser.page.wait_for_selector(".signInOut", timeout=5000)).click()
            await (await self.browser.page.wait_for_selector(".login input[type='email']", timeout=5000)).fill(
                username)
            await (await self.browser.page.wait_for_selector(".login input[type='password']", timeout=500)).fill(
                password)
            await (await self.browser.page.wait_for_selector(".login .signIn", timeout=500)).click()
            await (await self.browser.page.wait_for_selector("#startTestButton", timeout=500)).click()

        except TimeoutError as err:
            print(f"Error: {err}")

        finally:
            await self._choose_mode()
            await self._start_typing()

        await (await self.browser.page.wait_for_selector(".login .signInOut")).click()
        await (await self.browser.page.wait_for_selector(".login input[type='email']")).fill(username)
        await (await self.browser.page.wait_for_selector(".login input[type='password']")).fill(password)
        await (await self.browser.page.wait_for_selector(".login .signIn")).click()

    async def _start_typing(self) -> None:
        time.sleep(1)
        prompt = await self.get_prompt()
        print(prompt)
        random_num = random.randint(5, 7)
        another_num = random.randint(1, 50)
        if another_num == 1:
            print(another_num)
            pyautogui.typewrite(prompt, interval=0.055)
        else:
            print(another_num)
            pyautogui.typewrite(prompt, interval=random_num / 100)

        time.sleep(0.5)
        await self._next_game()

    # noinspection PyBroadException
    async def _next_game(self) -> None:
        try:
            time.sleep(1)
            await (await self.browser.page.wait_for_selector("#nextTestButton", timeout=1000)).click()
            await self._start_typing()

        except Exception as err:
            print(f"Failed to click next game button: {err}")
