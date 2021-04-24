Runs standard unittest discovery and testing, requiring less rain dance.

`neatest` replaces the shell command `python -m unittest discover ...`  with a brief programmatic call from Python code.

# Why

Testing should be simple. One line command. A really short line.

`python -m unittest ...` is too long. 

`run_tests.sh` is better. But POSIX-only and not pythonic.

`run_tests.py` is much better.

If your command looks like this

``` bash 
$ cd project_dir && python -m unittest discover -s ./mymodule -p '*.py' --buffer
```

use can replace it with `run_tests.py`:

``` python
#!/usr/bin/env python3
 
import unittest

suite = unittest.TestLoader().discover(
    start_dir="./mymodule",
    pattern="*.py")

result = unittest.TextTestRunner(buffer=True).run(suite)

if result.failures or result.errors:
    exit(1)
```

This script can be run with `python3 run_tests.py`. Now the command is short and cross-platform. 

But the code inside `run_tests.py` is long and not obvious. It is easier 
to copy this script to a new project than to recreate it.

So, here is the `neatest`. It makes the script even shorter.

```python
import neatest
neatest.pattern = "*.py"
neatest.start_dir = "./module"
neatest.run()
```

# Install

``` bash
pip3 install neatest
```

# Run tests

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


# Run tests from setup.py

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

