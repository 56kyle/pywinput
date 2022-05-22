
import win32api
import win32con
import win32gui

from pywinput.logger import log, logged
from pywinput.structures import *


class WindowClass:
    """A class that is equivalent to win32gui.PyWNDCLASS that automatically registers"""
    def __init__(self,
                 style: int,
                 cbWndExtra: int,
                 hInstance: int = None,
                 hIcon: int = None,
                 hCursor: int = None,
                 hbrBackground: int = None,
                 lpszMenuName: str = None,
                 lpszClassName: str = None,
                 lpfnWndProc: WNDPROC | dict = None):
        self.style = style
        self.cbWndExtra = cbWndExtra
        self.hInstance = hInstance if hInstance is not None else win32api.GetModuleHandle(None)
        self.hIcon = hIcon if hIcon is not None else 0
        self.hCursor = hCursor if hCursor is not None else 0
        self.hbrBackground = hbrBackground if hbrBackground is not None else 0
        self.lpszMenuName = lpszMenuName if lpszMenuName is not None else ''
        self.lpszClassName = lpszClassName if lpszClassName is not None else ''
        match lpfnWndProc:
            case WNDPROC():
                self.lpfnWndProc = lpfnWndProc
            case dict():
                self.lpfnWndProc = lpfnWndProc
            case None:
                self.lpfnWndProc = {
                    win32con.WM_DESTROY: self.on_destroy,
                    win32con.WM_COMMAND: self.on_command,
                    win32con.WM_USER + 20: self.on_taskbar_notify,
                }
            case _:
                raise TypeError(f'lpfnWndProc must be a WNDPROC, dict, or None, not {type(lpfnWndProc)}')

        self.register()

    def __del__(self):
        self.unregister()

    def __str__(self):
        return self.lpszClassName

    def __repr__(self):
        return f'<WindowClass(lpszClassName={self.lpszClassName})>'

    def __eq__(self, other):
        match other:
            case WindowClass():
                return self.lpszClassName == other.lpszClassName
            case str():
                return self.lpszClassName == other
            case _:
                raise TypeError(f'WindowClass.__eq__() can only compare to WindowClass or str, not {type(other)}')

    @logged
    def register(self):
        # Check if the class is already registered
        try:
            wc = win32gui.WNDCLASS()
            wc.style = self.style
            wc.cbWndExtra = self.cbWndExtra
            wc.hInstance = self.hInstance
            wc.hIcon = self.hIcon
            wc.hCursor = self.hCursor
            wc.hbrBackground = self.hbrBackground
            wc.lpszMenuName = self.lpszMenuName
            wc.lpszClassName = self.lpszClassName
            wc.lpfnWndProc = self.lpfnWndProc
            win32gui.RegisterClass(wc)
        except Exception as e:
            if e.args[0] != 1410:
                raise e

    @logged
    def unregister(self):
        win32gui.UnregisterClass(self.lpszClassName, self.hInstance)

    @logged
    def on_destroy(self, hwnd: int, message: int, wparam: int, lparam: int):
        win32gui.PostQuitMessage(0)

    @logged
    def on_command(self, hwnd: int, message: int, wparam: int, lparam: int):
        pass

    @logged
    def on_taskbar_notify(self, hwnd: int, message: int, wparam: int, lparam: int):
        pass

