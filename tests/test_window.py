

import win32api
import win32con
import win32gui

import pytest

from pywinput.window import Window


def test_window_init(example_window):
    """Tests the 'Window.__init__' method."""
    assert Window(example_window.hwnd) == example_window

def test_window_create(example_window_class):
    """Tests the 'Window.get_title' method."""
    win = Window.create(
        x=10,
        y=20,
        width=30,
        height=40,
    )
    assert win.text == ''
    assert win.x == 10
    assert win.y == 20
    assert win.width == 30
    assert win.height == 40

def test_window_find(example_window):
    """Tests the 'Window.find' method."""
    win = Window.find('Example Window')
    assert win == example_window

def test_window_str(example_window):
    """Tests the '__str__' method."""
    assert str(example_window) == example_window.text

def test_window_repr(example_window):
    """Tests the '__repr__' method."""
    assert repr(example_window) == f'<Window(hwnd={example_window.hwnd})>'

def test_window_text_getter(example_window):
    """Tests the 'Window.text' property."""
    assert example_window.text == 'My win32api app'

def test_window_text_setter(example_window):
    """Tests the 'Window.text' property."""
    original_text = example_window.text
    example_window.text = 'New Window'
    assert example_window.text == 'New Window'
    example_window.text = original_text
    assert example_window.text == original_text








