import random
import time

import pyautogui

from bot.Browser import Browser


class Bot:
    def __init__(self):
        self.browser = Browser()

    async def init(self, username: str, password: str):
        await self.browser.initialize()
        await self._sign_in(username, password)

        # await self._choose_mode()
        # await self._start_typing()

    async def get_prompt(self):
        words = await (await self.browser.page.query_selector("#words")).query_selector_all(".word")
        sentence = []

        for i in range(len(words)):
            word = await words[i].text_content()
            if random.random() < 0.05:
                index = random.randrange(len(word))
                new_char = chr(random.randint(32, 126))
                word = word[:index] + new_char + word[index + 1:]
            sentence.append(word)

        print(sentence, "SENTENCE")

        return ' '.join(sentence)

    async def _choose_mode(self):
        try:
            await (await self.browser.page.wait_for_selector(".textButton[mode='words']", timeout=1000)).click()

        except TimeoutError as err:
            print(f"Error: {err}")

    async def _sign_in(self, username: str, password: str):
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

    async def _start_typing(self):
        time.sleep(1)
        prompt = await self.get_prompt()
        print(prompt)
        random_num = random.randint(6, 9)
        pyautogui.typewrite(prompt, interval=random_num / 100)
        time.sleep(0.5)
        await self._next_game()

    # noinspection PyBroadException
    async def _next_game(self):
        try:
            await (await self.browser.page.wait_for_selector("#nextTestButton", timeout=1000)).click()
        except Exception:
            try:
                time.sleep(1)
                await (await self.browser.page.wait_for_selector("#nextTestButton", timeout=1000)).click()

            except Exception as err:
                print(f"Failed to click next game button: {err}")
        await self._start_typing()
