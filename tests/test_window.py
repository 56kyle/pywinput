

import win32api
import win32con
import win32gui

import pytest

from pywinput.window import Window


def test_window_init(example_window):
    """Tests the 'Window.__init__' method."""
    assert Window(example_window.hwnd) == example_window

def test_window_str(example_window):
    """Tests the '__str__' method."""
    assert str(example_window) == example_window.text

def test_window_repr(example_window):
    """Tests the '__repr__' method."""
    assert repr(example_window) == f'<Window(hwnd={example_window.hwnd})>'

def test_window_eq(example_window):
    """Tests the 'Window.__eq__' method."""
    assert example_window == Window(example_window.hwnd)

def test_window_create(example_window_class):
    """Tests the 'Window.get_title' method."""
    win = Window.create(
        windowClass=None,
        windowTitle='foo',
        style=win32con.WS_OVERLAPPEDWINDOW,
        x=100,
        y=200,
        width=400,
        height=400,
    )
    assert win.text == 'foo'
    assert win.x == 100
    assert win.y == 200
    assert win.width == 400
    assert win.height == 400

def test_window_find(example_window):
    """Tests the 'Window.find' method."""
    win = Window.find('Example Window')
    assert win == example_window

def test_window_text_getter(example_window):
    """Tests the 'Window.text' property."""
    assert example_window.text == 'Example Window'

def test_window_text_setter(example_window):
    """Tests the 'Window.text' property."""
    original_text = example_window.text
    example_window.text = 'New Window'
    assert example_window.text == 'New Window'
    example_window.text = original_text
    assert example_window.text == original_text

def test_rect_getter(example_window):
    example_window.rect = (100, 200, 500, 600)
    assert example_window.rect == (100, 200, 500, 600)

def test_rect_setter(example_window):
    example_window.rect = (200, 300, 500, 500)
    assert example_window.rect == (200, 300, 500, 500)
    example_window.rect = (100, 200, 500, 600)
    assert example_window.rect == (100, 200, 500, 600)

def test_width_getter(example_window):
    example_window.rect = (100, 200, 500, 600)
    assert example_window.width == 400

def test_width_setter(example_window):
    example_window.rect = (100, 200, 500, 600)
    assert example_window.width == 400
    example_window.width = 700
    assert example_window.width == 700
    assert example_window.x == 100

def test_height_getter(example_window):
    example_window.rect = (100, 200, 500, 600)
    assert example_window.height == 400

def test_height_setter(example_window):
    example_window.rect = (100, 200, 500, 600)
    assert example_window.height == 400
    example_window.height = 700
    assert example_window.height == 700
    assert example_window.y == 200

def test_x_getter(example_window):
    example_window.rect = (100, 200, 500, 600)
    assert example_window.x == 100

def test_x_setter(example_window):
    example_window.rect = (100, 200, 500, 600)
    assert example_window.x == 100
    example_window.x = 300
    assert example_window.x == 300
    assert example_window.width == 400

def test_y_getter(example_window):
    example_window.rect = (100, 200, 500, 600)
    assert example_window.y == 200

def test_y_setter(example_window):
    example_window.rect = (100, 200, 500, 600)
    assert example_window.y == 200
    example_window.y = 300
    assert example_window.y == 300
    assert example_window.height == 400

def test_visible_getter(example_window):
    example_window.visible = True
    assert example_window.visible

def test_visible_setter(example_window):
    example_window.visible = True
    assert example_window.visible
    example_window.visible = False
    assert not example_window.visible

def test_show(example_window):
    example_window.visible = False
    assert not example_window.visible
    example_window.show()
    assert example_window.visible

def test_hide(example_window):
    example_window.visible = True
    assert example_window.visible
    example_window.hide()
    assert not example_window.visible

def test_enabled_getter(example_window):
    example_window.enabled = False
    assert not example_window.enabled

def test_enabled_setter(example_window):
    example_window.enabled = False
    assert not example_window.enabled
    example_window.enabled = True
    assert example_window.enabled

def test_enable(example_window):
    example_window.enabled = False
    assert not example_window.enabled
    example_window.enable()
    assert example_window.enabled

def test_disable(example_window):
    example_window.enabled = True
    assert example_window.enabled
    example_window.disable()
    assert not example_window.enabled

def test_focused_getter(example_window, other_window):
    other_window.focus()
    assert not example_window.focused

def test_focus(example_window, other_window):
    other_window.focus()
    assert not example_window.focused
    example_window.focus()
    assert example_window.focused

def test_active_getter(example_window, other_window):
    other_window.activate()
    assert not example_window.active

def test_activate(example_window, other_window):
    other_window.activate()
    assert not example_window.active
    example_window.activate()
    assert example_window.active

def test_close(example_window):
    example_window.close()

def test_update(example_window):
    example_window.update()

def test_send_message(example_window):
    pass

def test_post_message(example_window):
    pass

def test_flash(example_window):
    example_window.flash()
