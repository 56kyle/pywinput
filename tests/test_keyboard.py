
import pytest
import win32api
import win32con
import win32gui


def test_keyboard_send(example_window):
    example_window.keyboard.send('a')

