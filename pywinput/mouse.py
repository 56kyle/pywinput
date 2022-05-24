import win32api
import win32con
import win32gui
import mouse
import time

from typing import Tuple


class Mouse:
    def __init__(self, window):
        self.window = window

    @property
    def position(self) -> Tuple[int, int]:
        return win32gui.GetCursorPos()

    def pressed(self, key=win32con.VK_LBUTTON) -> bool:
        return win32api.GetKeyState(key) & 0x8000

    def click(self, button=win32con.VK_LBUTTON):
        self.press(button)
        self.release(button)

    def drag(self, start_x, start_y, end_x, end_y, absolute=True, duration=0):
        if self.pressed:
            self.release()
        self.move(start_x, start_y, absolute, 0)
        self.press()
        self.move(end_x, end_y, absolute, duration)
        self.release()

    def move(self, x, y, absolute=True, duration=0):
        position_x, position_y = self.position

        if not absolute:
            x = position_x + x
            y = position_y + y

        if duration:
            start_x = position_x
            start_y = position_y
            dx = x - start_x
            dy = y - start_y

            if dx == 0 and dy == 0:
                time.sleep(duration)
            else:
                # 120 movements per second.
                # Round and keep float to ensure float division in Python 2
                steps = max(1.0, float(int(duration * 120.0)))
                for i in range(int(steps) + 1):
                    self.move(start_x + dx * i / steps, start_y + dy * i / steps)
                    time.sleep(duration / steps)
        else:
            self.window.post_message(win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))

    def scroll(self, delta=1):
        self.window.post_message(win32con.WM_MOUSEWHEEL, delta, 0)

    def press(self, button=win32con.VK_LBUTTON):
        match button:
            case win32con.VK_LBUTTON:
                self.window.post_message(win32con.WM_LBUTTONDOWN, 0, win32api.MAKELONG(*self.position))
            case win32con.VK_RBUTTON:
                self.window.post_message(win32con.WM_RBUTTONDOWN, 0, win32api.MAKELONG(*self.position))
            case win32con.VK_MBUTTON:
                self.window.post_message(win32con.WM_MBUTTONDOWN, 0, win32api.MAKELONG(*self.position))
            case _:
                raise ValueError('Invalid button')

    def release(self, button=win32con.VK_LBUTTON):
        match button:
            case win32con.VK_LBUTTON:
                self.window.post_message(win32con.WM_LBUTTONUP, 0, 0)
            case win32con.VK_RBUTTON:
                self.window.post_message(win32con.WM_RBUTTONUP, 0, 0)
            case win32con.VK_MBUTTON:
                self.window.post_message(win32con.WM_MBUTTONUP, 0, 0)
            case _:
                raise ValueError('Invalid button')

    def double_click(self):
        self.click()
        self.click()




