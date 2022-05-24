
import pytest
import win32api
import win32con
import win32gui

import pywinput.keyboard



def test_keyboard_send(example_window):
    keyboard.send()

