Runs standard unittest discovery and testing, requiring less rain dance.

`neatest` replaces the call to the shell `python -m unittest discover ...` command with a programmaic call like

```python
import neatest
neatest.run()
```

-------------------------------------------------------------------------------

Calling `python -m unittest ...` can get tedious. It turns out pretty quickly that you prefer to run 
some kind of `runtests.sh` instead of the command.

But Python is cross-platform, and Bash is not.
An executable `runtests.py` would be much more pythonic in all senses.

In fact, you really can replace

``` bash
$ cd project_dir && python -m unittest discover -s . -p '*.py' --buffer
```

with `project_dir/runtests.py`:

``` python
#!/usr/bin/env python3
 
import unittest
from pathlib import Path

parent_dir = Path(__file__).parent
init_py, = parent_dir.glob("*/__init__.py")

suite = unittest.TestLoader().discover(
    top_level_dir=str(parent_dir),
    start_dir=str(init_py.parent),
    pattern="*.py")

result = unittest.TextTestRunner(buffer=True).run(suite)

if result.failures or result.errors:
    exit(1)
```

It can be run on any OS with `python3 runtests.py`.

But now we have a lot of boilerplate code.

So, here is the `neatest`. It eliminates the need of boilerplate and keeps the essence.  

## Run tests from terminal

#### project_dir / my_test.py

``` python3
import neatest

neatest.pattern = '*.py'  # optional initialization

if __name__ == "__main__":
    neatest.run()
```

#### Terminal

``` bash
$ python my_test.py
```

The good news is that you don't need to be in the project directory.

``` bash
$ cd anywhere
$ python /path/to/project_dir/my_test.py  # it works
```


## Run tests from setup.py

#### project_dir / my_test.py

``` python3
import neatest

neatest.pattern = '*.py'  # optional initialization
```

#### project_dir / setup.py

``` python3 
setup(
  ...
  test_suite='my_test.neatest.suite',
)
```

#### Terminal

``` bash
$ cd project_dir
$ python setup.py test
```

