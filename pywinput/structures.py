

import win32api
import win32con
import win32gui


from ctypes.wintypes import *
from ctypes import Structure, WINFUNCTYPE, POINTER
from typing import NamedTuple


HCURSOR = HICON
LRESULT = POINTER(LONG)
WNDPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)


class WINDOWINFO(Structure):
    """https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-windowinfo"""
    _fields_ = [
        ('cbSize', DWORD),
        ('rcWindow', RECT),
        ('rcClient', RECT),
        ('dwStyle', DWORD),
        ('dwExStyle', DWORD),
        ('dwWindowStatus', DWORD),
        ('cxWindowBorders', UINT),
        ('cyWindowBorders', UINT),
        ('atomWindowType', ATOM),
        ('wCreatorVersion', WORD),
    ]


class WINDOWPLACEMENT(Structure):
    """https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-windowplacement"""
    _fields_ = [
        ('length', UINT),
        ('flags', UINT),
        ('showCmd', UINT),
        ('ptMinPosition', POINT),
        ('ptMaxPosition', POINT),
        ('rcNormalPosition', RECT),
        ('rcDevice', RECT),
    ]


SWP_DRAWFRAME = 0x0020
SWP_FRAMECHANGED = 0x0020
SWP_HIDEWINDOW = 0x0080
SWP_NOACTIVATE = 0x0010
SWP_NOCOPYBITS = 0x0100
SWP_NOMOVE = 0x0002
SWP_NOOWNERZORDER = 0x0200
SWP_NOREDRAW = 0x0008
SWP_NOREPOSITION = 0x0200
SWP_NOSENDCHANGING = 0x0400
SWP_NOSIZE = 0x0001
SWP_NOZORDER = 0x0004
SWP_SHOWWINDOW = 0x0040

class WINDOWPOS(Structure):
    """https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-windowpos"""
    _fields_ = [
        ('hwnd', HWND),
        ('hwndInsertAfter', HWND),  # Position in Z order, may be hwnd of another window or a special value
        ('x', UINT),  # x position
        ('y', UINT),  # y position
        ('cx', UINT),  # width
        ('cy', UINT),  # height
        ('flags', UINT),  # May be one or more of the above flags
    ]


class WNDCLASSA(Structure):
    """https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-windowclassa"""
    _fields_ = [
        ('style', UINT),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', INT),
        ('cbWndExtra', INT),
        ('hInstance', HINSTANCE),
        ('hIcon', HICON),
        ('hCursor', HCURSOR),
        ('hbrBackground', HBRUSH),
        ('lpszMenuName', LPCSTR),
        ('lpszClassName', LPCSTR),
    ]


class WNDCLASSEXA(Structure):
    """https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-windowclassexa"""
    _fields_ = [
        ('cbSize', UINT),
        ('style', UINT),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', INT),
        ('cbWndExtra', INT),
        ('hInstance', HINSTANCE),
        ('hIcon', HICON),
        ('hCursor', HCURSOR),
        ('hbrBackground', HBRUSH),
        ('lpszMenuName', LPCSTR),
        ('lpszClassName', LPCSTR),
        ('hIconSm', HICON),
    ]


class WNDCLASSEXW(Structure):
    """https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-windowclassexw"""
    _fields_ = [
        ('cbSize', UINT),
        ('style', UINT),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', INT),
        ('cbWndExtra', INT),
        ('hInstance', HINSTANCE),
        ('hIcon', HICON),
        ('hCursor', HCURSOR),
        ('hbrBackground', HBRUSH),
        ('lpszMenuName', LPCWSTR),
        ('lpszClassName', LPCWSTR),
        ('hIconSm', HICON),
    ]


class WNDCLASSW(Structure):
    """https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-windowclassw"""
    _fields_ = [
        ('style', UINT),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', INT),
        ('cbWndExtra', INT),
        ('hInstance', HINSTANCE),
        ('hIcon', HICON),
        ('hCursor', HCURSOR),
        ('hbrBackground', HBRUSH),
        ('lpszMenuName', LPCWSTR),
        ('lpszClassName', LPCWSTR),
    ]

