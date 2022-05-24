

import pytest
import win32gui

from pywinput.structures import *
from pywinput.window import Window, create, find
from pywinput.window_class import WindowClass


@pytest.fixture(scope='session')
def example_window_class() -> WindowClass:
    return WindowClass(
        style=win32con.CS_HREDRAW | win32con.CS_VREDRAW,
        cbWndExtra=win32con.DLGWINDOWEXTRA,
        lpszClassName='Example Window Class',
    )


@pytest.fixture(scope="session")
def example_window(example_window_class) -> Window:
    return create(
        windowClass=example_window_class,
        windowTitle='Example Window',
    )


@pytest.fixture(scope="session")
def other_window(example_window_class) -> Window:
    return create(
        windowClass=example_window_class,
        windowTitle='Other Window',
    )




