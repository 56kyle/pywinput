

import pytest
from pywinput.window import Window


@pytest.fixture(scope="session")
def example_window():
    return Window.create('Example Window', 100, 200, 300, 400)


