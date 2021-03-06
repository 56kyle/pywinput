
import pytest
import pywintypes
import win32api
import win32con
import win32gui

from pywinput.window import Window
from pywinput.window_class import WindowClass


def test_window_class_init():
    win_cls = WindowClass(
        style=win32con.CS_HREDRAW | win32con.CS_VREDRAW,
        cbWndExtra=win32con.DLGWINDOWEXTRA,
    )
    assert win_cls.style == win32con.CS_HREDRAW | win32con.CS_VREDRAW
    assert win_cls.cbWndExtra == win32con.DLGWINDOWEXTRA

def test_window_class_del():
    temp_win_cls = WindowClass(
        style=win32con.CS_HREDRAW | win32con.CS_VREDRAW,
        cbWndExtra=win32con.DLGWINDOWEXTRA,
        lpszClassName='TempWndClass'
    )
    del temp_win_cls

def test_window_class_str(example_window_class):
    assert str(example_window_class) == example_window_class.lpszClassName

def test_window_class_repr(example_window_class):
    assert repr(example_window_class) == f'<WindowClass(lpszClassName={example_window_class.lpszClassName})>'

def test_window_class_eq(example_window_class):
    assert example_window_class == example_window_class
    assert example_window_class == example_window_class.lpszClassName

def test_window_class_register(example_window):
    assert win32gui.GetClassName(example_window.hwnd)

def test_window_class_unregister(example_window_class):
    temp_window = Window.create(
        windowClass=example_window_class,
        windowTitle='Temp Window',
    )
    with pytest.raises(Exception) as excinfo:
        example_window_class.unregister()
        assert '1412' in str(excinfo.value)
    temp_window.close()

def test_window_class_on_destroy(example_window_class):
    assert example_window_class.on_destroy is not None
    example_window_class.on_destroy(0, 0, 0, 0)

def test_window_class_on_command(example_window_class):
    assert example_window_class.on_command is not None
    example_window_class.on_command(0, 0, 0, 0)

def test_window_class_on_taskbar_notify(example_window_class):
    assert example_window_class.on_taskbar_notify is not None
    example_window_class.on_taskbar_notify(0, 0, 0, 0)

