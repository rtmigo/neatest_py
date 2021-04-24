# [neatest](https://github.com/rtmigo/neatest_py)
Runs standard Python unittest discovery and testing. Provides a more convenient way of configuring
the tests. 

It replaces the shell command `python -m unittest discover ...`  with a brief programmatic call from Python code.

# Why

Testing should be simple. One line command. A really short line.

`python -m unittest discover ...` is too long. 

`run_tests.sh` is better. But not pythonic and not cross-platform.

`run_tests.py` is much better.

For example, if your command looks like this

``` bash 
$ cd project_dir && python -m unittest discover -s ./mymodule -p '*_test.py' --buffer
```

you can replace it with `run_tests.py`:

``` python3
import neatest
neatest.pattern = "*_test.py"
neatest.start_dir = "./module"
neatest.run()
```

This script can be run with `python3 run_tests.py`. Now the command is short and cross-platform.

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

# Differences from "-m unittest discover"

## pattern

`neatest` searches for tests in all `*.py` files. Any `TestCase` in the code is considered a test to be run.

Standard `unittest discover` searches only for tests in files named `test*.py`.

## start_dir and top_level_dir

If not specified, `neatest` find the first directory containing `__init__.py` and consider it the `start_dir` 
(the module containing the tests).

The `top_level_dir` by default is the current directory, and it does not depend on `start_dir`.

It works well with package structure like that:

```
project_dir
  my_module
    tests
      __init__.py
      test_a.py
      test_b.py 
    __init__.py
    code1.py
    code2.py
  setup.py
```

If we run testing with `project_dir` being the current directory, the tests will be found inside `my_module`. The 
`project_dir` will remain the current directory for `import`s.

---

Standard `unittest discover` assumes that the starting directory is the current directory. If run from the `project_dir` 
it will not find any tests, unless you explicitly specify that the `start_dir` is `my_module`. But when you specify 
`start_dir`, the `top_level_dir` also changes to the same value. If you want to keep `top_level_dir` 
as the `project_dir`, you will have to specify this explicitly as well.

For `neatest` to behave as standard, just set `neatest.start_dir="."` and `neatest.top_level_dir=None`