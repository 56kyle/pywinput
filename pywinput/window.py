
import win32api
import win32con
import win32gui
import win32ui

from typing import NamedTuple

from pywinput.logger import log, logged
from pywinput.structures import *
from pywinput.window_class import WindowClass


class Window:
    def __init__(self, hwnd):
        self.hwnd = hwnd

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'<Window(hwnd={self.hwnd})>'

    def __eq__(self, other):
        if isinstance(other, Window):
            return self.hwnd == other.hwnd
        return False

    @classmethod
    @logged
    def create(cls,
               windowClass: int | str | WindowClass = None,
               windowTitle: str = '',
               style: int = win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.WS_THICKFRAME | win32con.WS_MINIMIZEBOX | win32con.WS_MAXIMIZEBOX,
               x: int = win32con.CW_USEDEFAULT,
               y: int = win32con.CW_USEDEFAULT,
               width: int = win32con.CW_USEDEFAULT,
               height: int = win32con.CW_USEDEFAULT,
               parent: int = None,
               menu: int = None,
               hInstance: int = win32api.GetModuleHandle(None),
               reserved: None = None,
               ):
        if windowClass is None:
            windowClass = WindowClass(
                style=win32con.CS_HREDRAW | win32con.CS_VREDRAW,
                cbWndExtra=win32con.DLGWINDOWEXTRA,
                lpszClassName='MyWndClass',
                hInstance=hInstance,
            )

        lpszClassName = windowClass.lpszClassName if isinstance(windowClass, WindowClass) else windowClass
        hwnd = win32gui.CreateWindow(
            lpszClassName,
            windowTitle,
            style,
            x,
            y,
            width,
            height,
            parent,
            menu,
            hInstance,
            reserved
        )
        win32gui.UpdateWindow(hwnd)
        return cls(hwnd)

    @classmethod
    @logged
    def find(cls, title):
        hwnd: HWND | None = win32gui.FindWindow(None, title)
        if hwnd:
            return cls(hwnd)
        return None

    @logged
    def close(self):
        win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)

    @property
    def text(self):
        return win32gui.GetWindowText(self.hwnd)

    @text.setter
    def text(self, text):
        win32gui.SetWindowText(self.hwnd, text)

    @property
    def rect(self):
        return win32gui.GetWindowRect(self.hwnd)

    @rect.setter
    def rect(self, rect):
        win32gui.MoveWindow(self.hwnd, rect[0], rect[1], rect[2], rect[3], True)

    @property
    def width(self):
        return self.rect[2] - self.rect[0]

    @width.setter
    def width(self, width):
        self.rect = (self.rect[0], self.rect[1], self.rect[0] + width, self.rect[3])

    @property
    def height(self):
        return self.rect[3] - self.rect[1]

    @height.setter
    def height(self, height):
        self.rect = (self.rect[0], self.rect[1], self.rect[2], self.rect[1] + height)

    @property
    def x(self):
        return self.rect[0]

    @x.setter
    def x(self, x):
        self.rect = (x, self.rect[1], self.width + x, self.rect[3])

    @property
    def y(self):
        return self.rect[1]

    @y.setter
    def y(self, y):
        self.rect = (self.rect[0], y, self.rect[2], self.height + y)

    @property
    def visible(self):
        return win32gui.IsWindowVisible(self.hwnd)

    @logged
    def show(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

    @logged
    def hide(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_HIDE)

    @property
    def enabled(self):
        return win32gui.IsWindowEnabled(self.hwnd)

    @logged
    def enable(self):
        win32gui.EnableWindow(self.hwnd)

    @logged
    def disable(self):
        win32gui.EnableWindow(self.hwnd, False)

    @property
    def focused(self):
        return win32gui.GetForegroundWindow() == self.hwnd

    def focus(self):
        win32gui.SetForegroundWindow(self.hwnd)

    @property
    def active(self):
        return win32gui.GetActiveWindow() == self.hwnd

    def activate(self):
        win32gui.SetActiveWindow(self.hwnd)

    @logged
    def close(self):
        win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)

    @logged
    def update(self):
        win32gui.UpdateWindow(self.hwnd)

    @logged
    def send_message(self, message, wparam, lparam):
        win32gui.SendMessage(self.hwnd, message, wparam, lparam)

    @logged
    def post_message(self, message, wparam, lparam):
        win32gui.PostMessage(self.hwnd, message, wparam, lparam)


if __name__ == '__main__':
    print(win32gui.WNDCLASS().hIcon)





