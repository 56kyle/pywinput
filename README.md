
# Pywinput
A wrapper for pywin32 that allows for simulating keyboard and mouse input within background windows

## Installation

#### Pip

```
pip install pywinput
```

#### Poetry
    
```
poetry add pywinput
```


## Usage

```python
from pywinput import Window, Key, Button

if __name__ == '__main__':
    win = Window.create(
        title='My Test Window',
        x=400,
        y=400,
        width=200,
        height=200,
    )
    win.show()
    win.text = 'My new window title'
    win.s
```






