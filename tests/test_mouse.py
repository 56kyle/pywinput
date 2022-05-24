
import pytest

from pywinput.mouse import Mouse


def test_mouse_click(example_window):
    example_window.mouse.click()
