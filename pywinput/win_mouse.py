import win32api
import win32con
import win32gui
import time

from typing import Tuple

from pywinput.constants import *


class Mouse:
    def __init__(self, window):
        self.window = window

    @staticmethod
    def as_long(position):
        return win32api.MAKELONG(*position)

    def from_client(self, position):
        return position[0] - self.window.client_x, position[1] - self.window.client_y

    @property
    def position(self) -> Tuple[int, int]:
        return win32gui.GetCursorPos()

    @property
    def position_long_from_client(self):
        return self.as_long(self.from_client(self.position))

    def pressed(self, key=Button.LEFT) -> bool:
        return win32api.GetKeyState(key) & 0x8000

    def click(self, button=Button.LEFT):
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
            self.window.post_message(win32con.WM_MOUSEMOVE, 0, self.position_long_from_client)

    def scroll(self, delta=1):
        self.window.post_message(win32con.WM_MOUSEWHEEL, delta, 0)

    def press(self, button=Button.LEFT, modifiers=0x0000):
        match button:
            case Button.LEFT:
                self.window.post_message(Message.WM_LBUTTONDOWN, modifiers, self.position_long_from_client)
            case Button.RIGHT:
                self.window.post_message(Message.WM_RBUTTONDOWN, modifiers, self.position_long_from_client)
            case Button.MIDDLE:
                self.window.post_message(Message.WM_MBUTTONDOWN, modifiers, self.position_long_from_client)
            case Button.X1:
                # 0x0001 means the first X button
                self.window.post_message(Message.WM_XBUTTONDOWN, modifiers | 0x0001, self.position_long_from_client)
            case Button.X2:
                # 0x0002 means the second X button
                self.window.post_message(Message.WM_XBUTTONDOWN, modifiers | 0x0002, self.position_long_from_client)
            case _:
                raise ValueError('Invalid button')

    def release(self, button=Button.LEFT, modifiers=0x0000):
        match button:
            case Button.LEFT:
                self.window.post_message(Message.WM_LBUTTONUP, modifiers, self.position_long_from_client)
            case Button.RIGHT:
                self.window.post_message(Message.WM_RBUTTONUP, modifiers, self.position_long_from_client)
            case Button.MIDDLE:
                self.window.post_message(Message.WM_MBUTTONUP, modifiers, self.position_long_from_client)
            case Button.X1:
                # 0x0001 means the first X button
                self.window.post_message(Message.WM_XBUTTONUP, modifiers | 0x0001, self.position_long_from_client)
            case Button.X2:
                # 0x0002 means the second X button
                self.window.post_message(Message.WM_XBUTTONUP, modifiers | 0x0002, self.position_long_from_client)
            case _:
                raise ValueError('Invalid mouse button')

    def double_click(self):
        self.click()
        self.click()


if __name__ == '__main__':
    while True:
        pass




