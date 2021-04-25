# [neatest](https://github.com/rtmigo/neatest_py)

Runs unit tests with standard Python `unittest` module.

Can be conveniently invoked from Python code as `neatest.run(...)` instead of `python -m unittest discover ...`. 

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
     start_directory = "./mymodule" )
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

if __name__ == "__main__":
    # all arguments are optional
    neatest.run( pattern = '*_test.py'
                 verbosity = neatest.Verbosity.quiet )
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

# Arguments

Most of the arguments to the `neatest.run` method have the same names and 
meanings as the arguments of [unittest](https://docs.python.org/3/library/unittest.html#command-line-interface) and [unittest discover](https://docs.python.org/3/library/unittest.html#test-discovery). 


# Test discovery

The test discovery has different defaults than the standard [unittest discover](https://docs.python.org/3/library/unittest.html#test-discovery).

## Filenames

`neatest` searches for tests in all `*.py` files. Any `TestCase` in the code is
considered a test to be run.

So it's equivalent to setting `-p` like that

``` bash
$ python3 -m unittest discover -p "*.py"
```

## Directories

`neatest` assumes, that the current directory is the `top_level_directory`. It is the
base directory for all imports.

If the `start_directory` are not specified, `neatest` will find all the modules 
inside `top_level_directory` and will run tests for each of them.

```
top_level_directory
  module_a              # module_a will be tested
    __init__.py
  module_b              # module_b will be tested
    __init__.py
  module_c              # module_c will be tested
    __init__.py
    submodule           # will be tested as a part of module_c 
      __init__.py         
  subdir                # subdir is not a module
      module_d          # module_d will NOT be tested 
        __init__.py     # because it is not importable     
  setup.py
```

So running

``` bash
$ cd top_level_directory
$ neatest
```

is the same as running

``` bash
$ cd top_level_directory
$ python3 -m unittest discover -t . -s module_a -p "*.py"
$ python3 -m unittest discover -t . -s module_b -p "*.py"
$ python3 -m unittest discover -t . -s module_c -p "*.py"
```

