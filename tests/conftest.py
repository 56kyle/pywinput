

import pytest
import win32gui

from pywinput.structures import *
from pywinput.window import Window
from pywinput.window_class import WindowClass


@pytest.fixture(scope='session')
def example_window_class():
    return WindowClass(
        style=win32con.CS_HREDRAW | win32con.CS_VREDRAW,
        cbWndExtra=win32con.DLGWINDOWEXTRA,
        lpszClassName='MyWndClass',
    )


@pytest.fixture(scope="session")
def example_window(example_window_class):
    return Window.create(
        windowClass=example_window_class,
        windowTitle='My win32api app',
    )




