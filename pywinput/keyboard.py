
import win32api
import win32con
import win32gui

import keyboard
from pywinput.window import Window



def send(window: Window = None, hotkey=None, do_press=True, do_release=True):
    if window is None:
        return keyboard.send(hotkey, do_press=do_press, do_release=do_release)
    parsed = keyboard.parse_hotkey(hotkey)
    for step in parsed:
        press_method = keyboard._os_keyboard.press if window.focused else _post_key_press
        release_method = keyboard._os_keyboard.release if window.focused else _post_key_release
        if do_press:
            for scan_codes in step:
                press_method(scan_codes[0])
        if do_release:
            for scan_codes in reversed(step):
                release_method(scan_codes[0])


press_and_release = send

def press(window: Window = None, scan_code: int = None):
    if window is None:
        return keyboard.press(scan_code)
    send(window, scan_code, do_press=True, do_release=False)

def release(window: Window = None, scan_code: int = None):
    if window is None:
        return keyboard.release(scan_code)
    send(window, scan_code, do_press=False, do_release=True)

def _post_key_press(window: Window, scan_code: int):
    window.post_message(win32con.WM_KEYDOWN, scan_code, 0)

def _post_key_release(window: Window, scan_code: int):
    window.post_message(win32con.WM_KEYUP, scan_code, 0)


