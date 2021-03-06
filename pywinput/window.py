
import keyboard

import win32api
import win32con
import win32gui


from typing import SupportsInt, Iterable

from pywintypes import *
from pywinput.constants import *
from pywinput.logger import log
from pywinput.structures import *
from pywinput.window_class import WindowClass


class Window:
    def __init__(self, hwnd: HWND = None):
        self.hwnd = hwnd if hwnd is not None else win32gui.GetForegroundWindow()

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

    @classmethod
    def create(cls,
               klass: int | str | WindowClass = None,
               title: str = '',
               style: int = win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.WS_THICKFRAME | win32con.WS_MINIMIZEBOX | win32con.WS_MAXIMIZEBOX,
               x: int = win32con.CW_USEDEFAULT,
               y: int = win32con.CW_USEDEFAULT,
               width: int = win32con.CW_USEDEFAULT,
               height: int = win32con.CW_USEDEFAULT,
               parent: int = None,
               menu: int = None,
               h_instance: int = win32api.GetModuleHandle(None),
               reserved: None = None,
               ):
        if klass is None:
            klass = WindowClass(
                style=win32con.CS_HREDRAW | win32con.CS_VREDRAW,
                cbWndExtra=win32con.DLGWINDOWEXTRA,
                lpszClassName='MyWndClass',
                hInstance=h_instance,
            )
        class_name = klass.lpszClassName if isinstance(klass, WindowClass) else klass
        hwnd = win32gui.CreateWindow(
            class_name, title, style, x, y, width, height, parent, menu, h_instance, reserved
        )
        win32gui.UpdateWindow(hwnd)
        return cls(hwnd)

    @classmethod
    def find(cls, title: str):
        hwnd: HWND | None = win32gui.FindWindow(None, title)
        if hwnd:
            return cls(hwnd)
        return None

    @property
    def text(self):
        return win32gui.GetWindowText(self.hwnd)

    @text.setter
    def text(self, text):
        win32gui.SetWindowText(self.hwnd, text)

    @staticmethod
    def _rect_to_points(rect: RECT):
        return POINT(rect[0], RECT[1]), POINT(rect[2], RECT[3])

    @staticmethod
    def _points_to_rect(top_left, bottom_right):
        return top_left[0], top_left[1], bottom_right[0], bottom_right[1]

    @property
    def rect(self) -> RECT:
        return win32gui.GetWindowRect(self.hwnd)

    @rect.setter
    def rect(self, rect: RECT):
        tl = win32gui.ScreenToClient(self.hwnd, (rect[0], rect[1]))
        br = win32gui.ScreenToClient(self.hwnd, (rect[2], rect[3]))
        c_rect = self._points_to_rect(tl, br)
        win32gui.MoveWindow(self.hwnd, c_rect[0], c_rect[1], c_rect[2] - c_rect[0], c_rect[3] - c_rect[1], True)

    @property
    def width(self) -> int:
        return self.rect[2] - self.rect[0]

    @width.setter
    def width(self, width: SupportsInt):
        self.rect = (self.rect[0], self.rect[1], self.rect[0] + int(width), self.rect[3])

    @property
    def height(self) -> int:
        return self.rect[3] - self.rect[1]

    @height.setter
    def height(self, height: SupportsInt):
        self.rect = (self.rect[0], self.rect[1], self.rect[2], self.rect[1] + int(height))

    @property
    def x(self) -> int:
        return self.rect[0]

    @x.setter
    def x(self, x: SupportsInt):
        self.rect = (x, self.rect[1], self.width + int(x), self.rect[3])

    @property
    def y(self) -> int:
        return self.rect[1]

    @y.setter
    def y(self, y: SupportsInt):
        self.rect = (self.rect[0], y, self.rect[2], self.height + int(y))

    @property
    def client_rect(self) -> RECT:
        return win32gui.GetClientRect(self.hwnd)

    @client_rect.setter
    def client_rect(self, rect: RECT):
        win32gui.MoveWindow(self.hwnd, rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1], True)

    @property
    def client_width(self) -> int:
        return self.client_rect[2] - self.client_rect[0]

    @client_width.setter
    def client_width(self, width: SupportsInt):
        self.client_rect = (self.client_rect[0], self.client_rect[1], self.client_rect[0] + int(width), self.client_rect[3])

    @property
    def client_height(self) -> int:
        return self.client_rect[3] - self.client_rect[1]

    @client_height.setter
    def client_height(self, height: SupportsInt):
        self.client_rect = (self.client_rect[0], self.client_rect[1], self.client_rect[2], self.client_rect[1] + int(height))

    @property
    def client_x(self) -> int:
        return self.client_rect[0]

    @client_x.setter
    def client_x(self, x: int):
        self.client_rect = (x, self.client_rect[1], self.client_width + x, self.client_rect[3])

    @property
    def client_y(self) -> int:
        return self.client_rect[1]

    @client_y.setter
    def client_y(self, y: int):
        self.client_rect = (self.client_rect[0], y, self.client_rect[2], self.client_height + y)

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
    def maximized(self) -> bool:
        return win32gui.GetWindowPlacement(self.hwnd)[1] == win32con.SW_MAXIMIZE

    @maximized.setter
    def maximized(self, maximized: bool):
        self.maximize() if maximized else self.restore()

    def maximize(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)

    @property
    def minimized(self) -> bool:
        return win32gui.GetWindowPlacement(self.hwnd)[1] == win32con.SW_MINIMIZE

    @minimized.setter
    def minimized(self, minimized: bool):
        self.minimize() if minimized else self.restore()

    def minimize(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)

    @property
    def restored(self) -> bool:
        return win32gui.GetWindowPlacement(self.hwnd)[1] == win32con.SW_SHOWNORMAL

    @restored.setter
    def restored(self, restored: bool):
        self.restore() if restored else self.minimize()

    def restore(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)

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

    def send(self, scan_code: int | str, do_press: bool = True, do_release: bool = True, modifiers: int = None, position: POINT = None):
        parsed = keyboard.parse_hotkey(scan_code)
        for step in parsed:
            if do_press:
                for scan_codes in step:
                    self._simulate(scan_codes[0], do_press, False, modifiers, position)
            if do_release:
                for scan_codes in reversed(step):
                    self._simulate(scan_codes[0], False, do_release, modifiers, position)

    def _simulate(self,
                  scan_code: int,
                  do_press: bool = True,
                  do_release: bool = True,
                  modifiers: int = None,
                  position: POINT = None):
        down_message = None
        up_message = None
        if Button.has_value(scan_code):
            # Mouse button
            modifiers = modifiers if modifiers is not None else self._get_mouse_modifiers()
            position = position if position is not None else self._get_mouse_client_position()
            down_message = button_down_msg[scan_code]
            up_message = button_up_msg[scan_code]
            if do_press:
                self.post_message(down_message, modifiers, win32api.MAKELONG(position[0], position[1]))
            if do_release:
                self.post_message(up_message, modifiers, win32api.MAKELONG(position[0], position[1]))
        elif Key.has_value(scan_code):
            # Keyboard button
            modifiers = modifiers if modifiers is not None else 0
            if do_press:
                self.post_message(win32con.WM_KEYDOWN, scan_code, modifiers)
            if do_release:
                self.post_message(win32con.WM_KEYUP, scan_code, modifiers)
        else:
            raise ValueError('Invalid scan code')

    def _get_mouse_modifiers(self):
        keyboard_state = win32api.GetKeyboardState()
        modifier_list = [
            keyboard_state[win32con.VK_CONTROL],
            keyboard_state[Button.LEFT],
            keyboard_state[Button.MIDDLE],
            keyboard_state[Button.RIGHT],
            keyboard_state[Key.VK_SHIFT],
            keyboard_state[Button.X1],
            keyboard_state[Button.X2],
        ]
        return sum(1 << i for i, v in enumerate(modifier_list) if v)

    def _get_mouse_screen_position(self):
        return win32api.GetCursorPos()

    def _get_mouse_client_position(self):
        return win32gui.ScreenToClient(self.hwnd, self._get_mouse_screen_position())


if __name__ == '__main__':
    win = Window()
    win.x = 0
    win.y = 0
    win.width = 40
    win.height = 40
    win.update()
