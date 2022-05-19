

import win32api
import win32con
import win32gui


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
    def create(cls,
               text: str,
               width: int,
               height: int,
               x: int = 0,
               y: int = 0,
               class_name: int | str = None):
        hwnd = win32gui.CreateWindow(
            class_name, text, win32con.WS_OVERLAPPEDWINDOW,
            x, y, width, height,
            0, 0, win32api.GetModuleHandle(None), None
        )
        win32gui.UpdateWindow(hwnd)
        return cls(hwnd)

    @classmethod
    def find(cls, title):
        return cls(win32gui.FindWindow(None, title))

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
    def visible(self):
        return win32gui.IsWindowVisible(self.hwnd)

    def show(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

    def hide(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_HIDE)

    @property
    def enabled(self):
        return win32gui.IsWindowEnabled(self.hwnd)

    def enable(self):
        win32gui.EnableWindow(self.hwnd)

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

    def close(self):
        win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)

    def update(self):
        win32gui.UpdateWindow(self.hwnd)

    def send_message(self, message, wparam, lparam):
        win32gui.SendMessage(self.hwnd, message, wparam, lparam)

    def post_message(self, message, wparam, lparam):
        win32gui.PostMessage(self.hwnd, message, wparam, lparam)







