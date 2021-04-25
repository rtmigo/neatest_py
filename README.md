# [neatest](https://github.com/rtmigo/neatest_py)

Runs standard Python unittest discovery and testing. Provides a more convenient
way of configuring the tests.

It replaces the shell command `python -m unittest discover ...`  with a brief
programmatic call from Python code.

# Why

Testing should be simple. One-line command. A really short line.

`python -m unittest discover ...` is too long.

`run_tests.sh` is better. But not pythonic and not cross-platform.

`run_tests.py` is much better.

For example, if your command looks like this

``` bash 
$ cd project_dir && python -m unittest discover -s ./mymodule -p '*_test.py' -t '.'
```

you can replace it with `run_tests.py`:

``` python3
from neatest import run

run( pattern = "*_test.py",
     start_dirs = ["./module"] )
```

This script can be run with `python3 run_tests.py`. Now the command is short and
cross-platform.

# Install

``` bash
pip3 install neatest
```

# Run

## Run tests with .py script

#### project_dir / run_tests.py

``` python3
from neatest import run

if __name__ == "__main__":
    # all arguments are optional
    run( pattern = '*_test.py'
         verbocity = 2 )
```

#### Terminal

``` bash
$ python3 run_tests.py
```

## Run tests from terminal

``` bash
$ neatest
```

is equivalent to running the script

``` python3
import neatest
neatest.run()
```



# Test discovery

## Filenames

`neatest` searches for tests in all `*.py` files. Any `TestCase` in the code is
considered a test to be run.

## Directories

`neatest` assumes, that the current directory is the `top_level_dir`. It is the
base directory for all imports.

If the `start_dirs` are not specified, `neatest` will find all the modules 
inside `top_level_dir` and will import tests from them.

In the following example, we will run tests for `module_a`, and then 
for `module_b`. 

```
project_dir
  module_a              <-- will be tested
    __init__.py
  module_b              <-- will be tested
    __init__.py
  setup.py
```

It is the same as running consequently

``` bash
$ cd project_dir
$ python3 -m unittest discover -t . -s module_a
$ python3 -m unittest discover -t . -s module_b
```

