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
import neatest
neatest.pattern = "*_test.py"
neatest.start_dir = "./module"
neatest.run()
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
import neatest

# optionally setting parameters
neatest.pattern = '*_test.py'
neatest.verbocity = 2

if __name__ == "__main__":
    neatest.run()
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

## Run tests with setup.py

This way of running tests is deprecated by `setuptools`, but still works.

#### project_dir / run_tests.py

``` python3
import neatest

# optionally setting parameters. 
# Setup.py will only respect parameters related to
# the test discovery (TestSuite initialization)
neatest.pattern = '*_test.py'  # will be used
neatest.verbocity = 2          # will be ignored 
```

#### project_dir / setup.py

``` python3 
setup(
  ...
  test_suite='run_tests.neatest.suite',
)
```

#### Terminal

``` bash
$ cd project_dir
$ python3 setup.py test
```

# Test discovery

## Filenames

`neatest` searches for tests in all `*.py` files. Any `TestCase` in the code is
considered a test to be run.

## Directories

`neatest` assumes, that the current directory is the `top_level_dir`. It is the
base directory for all imports.

The `start_dir` is the directory, containing the module with tests. `neatest`
will try to find this directory automatically.

In the following example, `neatest` will select the `my_module` because it is the top
level directory containing `__init__.py`, and no sibling directories contain an 
`__init__.py`.

```
project_dir
  subdir_a
    some_files
    but_no_init_py
  subdir_b
    some_files
    but_no_init_py
  my_module
    __init__.py
    code1.py
    code2.py
  setup.py
```

In the following example, `neatest` will select the `tests` module because of its name

```
project_dir
  tests
    __init__.py
    test_a.py
    test_b.py 
  my_module
    __init__.py
    code1.py
    code2.py
  setup.py
```

In the following example, `neatest` will stop with error. You should manually specify
the `start_dir`.

```
project_dir
  my_module_a
    __init__.py
  my_module_b
    __init__.py    
  setup.py
```

For `neatest` to behave as standard `unittest discover`,
set `neatest.start_dir="."` and `neatest.top_level_dir=None`.