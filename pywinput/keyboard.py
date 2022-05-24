
import win32api
import win32con
import win32gui

import keyboard


class Keyboard:
    def __init__(self, window):
        self.window = window

    def send(self, hotkey=None, do_press=True, do_release=True):
        parsed = keyboard.parse_hotkey(hotkey)
        for step in parsed:
            press_method = keyboard._os_keyboard.press if self.window.focused else self._post_key_press
            release_method = keyboard._os_keyboard.release if self.window.focused else self._post_key_release
            if do_press:
                for scan_codes in step:
                    press_method(scan_codes[0])
            if do_release:
                for scan_codes in reversed(step):
                    release_method(scan_codes[0])

    press_and_release = send

    def press(self, scan_code: int):
        self.send(scan_code, do_press=True, do_release=False)

    def release(self, scan_code: int):
        self.send(scan_code, do_press=False, do_release=True)

    def _post_key_press(self, scan_code: int):
        self.window.post_message(win32con.WM_KEYDOWN, scan_code, 0)

    def _post_key_release(self, scan_code: int):
        self.window.post_message(win32con.WM_KEYUP, scan_code, 0)


