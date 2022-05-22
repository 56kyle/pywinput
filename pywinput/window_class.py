
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

        self.wc = win32gui.WNDCLASS()
        self.wc.style = self.style
        self.wc.cbWndExtra = self.cbWndExtra
        self.wc.hInstance = self.hInstance
        self.wc.hIcon = self.hIcon
        self.wc.hCursor = self.hCursor
        self.wc.hbrBackground = self.hbrBackground
        self.wc.lpszMenuName = self.lpszMenuName
        self.wc.lpszClassName = self.lpszClassName
        self.wc.lpfnWndProc = self.lpfnWndProc

        self.register()

    def __del__(self):
        self.unregister()

    def __str__(self):
        return self.lpszClassName

    def register(self):
        # Check if the class is already registered
        try:
            win32gui.RegisterClass(self.wc)
        except Exception as e:
            if e.args[0] != 1410:
                raise e

    def unregister(self):
        win32gui.UnregisterClass(self.lpszClassName, self.hInstance)

    def on_destroy(self, hwnd: int, message: int, wparam: int, lparam: int):
        pass

    def on_command(self, hwnd: int, message: int, wparam: int, lparam: int):
        pass

    def on_taskbar_notify(self, hwnd: int, message: int, wparam: int, lparam: int):
        pass

