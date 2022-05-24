

import win32api
import win32con
import win32gui

from typing import SupportsInt

from pywinput.logger import log
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
        match other:
            case Window():
                return self.hwnd == other.hwnd
            case SupportsInt() | HWND():
                return self.hwnd == other
            case _:
                raise TypeError(f'Cannot compare {type(self)} to {type(other)}')

    @property
    def text(self):
        return win32gui.GetWindowText(self.hwnd)

    @text.setter
    def text(self, text):
        win32gui.SetWindowText(self.hwnd, text)

    @property
    def rect(self) -> RECT:
        return win32gui.GetWindowRect(self.hwnd)

    @rect.setter
    def rect(self, rect: RECT):
        win32gui.MoveWindow(self.hwnd, rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1], True)

    @property
    def width(self) -> int:
        return self.rect[2] - self.rect[0]

    @width.setter
    def width(self, width: SupportsInt):
        self.rect = (self.rect[0], self.rect[1], self.rect[0] + width, self.rect[3])

    @property
    def height(self) -> int:
        return self.rect[3] - self.rect[1]

    @height.setter
    def height(self, height: SupportsInt):
        self.rect = (self.rect[0], self.rect[1], self.rect[2], self.rect[1] + height)

    @property
    def x(self) -> int:
        return self.rect[0]

    @x.setter
    def x(self, x: SupportsInt):
        self.rect = (x, self.rect[1], self.width + x, self.rect[3])

    @property
    def y(self) -> int:
        return self.rect[1]

    @y.setter
    def y(self, y: SupportsInt):
        self.rect = (self.rect[0], y, self.rect[2], self.height + y)

    @property
    def visible(self) -> bool:
        return win32gui.IsWindowVisible(self.hwnd)

    @visible.setter
    def visible(self, visible: bool):
        self.show() if visible else self.hide()

    def show(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

    def hide(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_HIDE)

    @property
    def enabled(self) -> bool:
        return win32gui.IsWindowEnabled(self.hwnd)

    @enabled.setter
    def enabled(self, enabled: bool):
        self.enable() if enabled else self.disable()

    def enable(self) -> bool:
        return win32gui.EnableWindow(self.hwnd, True)

    def disable(self) -> bool:
        return win32gui.EnableWindow(self.hwnd, False)

    @property
    def focused(self) -> bool:
        return win32gui.GetForegroundWindow() == self.hwnd

    def focus(self):
        win32gui.SetForegroundWindow(self.hwnd)

    @property
    def captured(self):
        return win32gui.GetCapture() == self.hwnd

    def capture(self):
        win32gui.SetCapture(self.hwnd)

    @property
    def active(self) -> bool:
        return win32gui.GetActiveWindow() == self.hwnd

    def activate(self):
        win32gui.SetActiveWindow(self.hwnd)

    def close(self):
        win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)

    def update(self):
        win32gui.UpdateWindow(self.hwnd)

    def send_message(self, message: SupportsInt, wparam: int | str = None, lparam: int | str = None) -> LRESULT:
        return win32gui.SendMessage(self.hwnd, message, wparam, lparam)

    def post_message(self, message: SupportsInt, wparam: int = 0, lparam: int = 0):
        win32gui.PostMessage(self.hwnd, message, wparam, lparam)

    def flash(self, bInvert: SupportsInt = 0):
        win32gui.FlashWindow(self.hwnd, 1 if bInvert else 0)


def create(windowClass: int | str | WindowClass = None,
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
    className = windowClass.lpszClassName if isinstance(windowClass, WindowClass) else windowClass
    hwnd = win32gui.CreateWindow(
        className, windowTitle, style, x, y, width, height, parent, menu, hInstance, reserved
    )
    win32gui.UpdateWindow(hwnd)
    return Window(hwnd)


def find(title: str) -> Window | None:
    hwnd: HWND | None = win32gui.FindWindow(None, title)
    if hwnd:
        return Window(hwnd)
    return None

