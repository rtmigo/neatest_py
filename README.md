# [neatest](https://github.com/rtmigo/neatest_py)

Runs unit tests with standard Python `unittest` module.

Automates test discovery.

Can be conveniently invoked from Python code as `neatest.run(...)` method
instead of running `python -m unittest discover ...` in shell.

# Install

``` bash
pip3 install neatest
```

# Project layout

`neatest` discovers all classes inherited from `unittest.TestCase` within the
project. Test cases can be placed in **any .py file** inside **any directory**.
If you prefer to keep test cases in the "tests" directory with filenames
starting with "test", they will be discovered, because they are also "any
files in any directory".

You can use a simple project layout:

```
my_simple_project
    __init__.py     # tests can be placed here
    test_a.py       # tests can be placed here
    test_b.py       # tests can be placed here
    anything.py     # tests can be placed here
```

or a project with multiple packages:

```
my_complex_project
    package_a
        __init__.py         # tests can be placed here
        any_files.py        # tests can be placed here
        can_contain.py      # tests can be placed here
        tests_inside.py     # tests can be placed here
        ...
    package_b
        __init__.py         # tests can be placed here
        ...
    tests  
        __init__.py         # tests can be placed here
        test_something.py   # tests can be placed here
        test_anything.py    # tests can be placed here        
```

Subdirectories must be **importable** as packages from the project directory.

They are importable, when you can

``` bash
$ cd my_complex_project
$ python3 
```

and then in Python

``` python3
import package_a
import package_b
import tests 
```

# Run

## Run tests from command line

``` bash
$ cd my_complex_project
$ neatest
```

```
Package "package_a" contains 3 tests
Package "package_b" contains 4 tests
Package "tests" contains 16 tests
.....
----------------------------------------------------------------------
Ran 23 tests in 2.947s

OK
```

Add some options:

``` bash
$ cd my_complex_project
$ neatest --start-directory tests --verbose
```

See all possible options:

``` bash
$ neatest --help
```


## Run tests from .py script

#### Create a script

For example, `run_tests.py`:

``` python3
import neatest
neatest.run()
```

#### Run the script

``` bash
$ cd my_complex_project
$ python3 path/to/run_tests.py
```

The idea is to use single `.py` script to run the tests (instead of `.sh`, `.bat` or `.cfg`). 
Python script is readable, and it's portable as the Python itself.

You can specify all the options available to `neatest` command-line tool as 
arguments to `neatest.run` method:

``` python3
import neatest
neatest.run(start_directory="tests",
            verbosity=neatest.Verbosity.verbose)
```

# Arguments

## tests_require

You can specify dependencies to be installed with `pip install` before testing.
These dependencies are presumably missing from `requirements.txt` and `setup.py`
as they are not needed in production.

``` python
neatest.run(tests_require=['requests', 'lxml']) 
```

``` bash
$ neatest -r requests -r lxml
```

This is the equivalent of the deprecated argument `tests_require`
from `setuptools.setup`.

# warnings

By default, warnings caught during testing are printed to the stdout.

### warnings: ignore

In this mode warnings will not be displayed.

``` python
neatest.run(warnings=neatest.Warnings.ignore)
```
``` bash
$ neatest --warnings ignore
```



### warnings: fail

In this mode warnings will be treated as errors. If at least one warning appears
during testing, it will cause the testing to fail (with exception or non-zero
return code).

``` python
neatest.run(warnings=neatest.Warnings.fail)
```
``` bash
$ neatest --warnings fail
```


# Test discovery

## Filenames

`neatest` searches for tests in all `*.py` files.

The same can be achieved with standard `unittest` like this:

``` bash
$ python3 -m unittest discover -p "*.py"
```

## Directories

`neatest` assumes, that the current directory is the project directory. It is
the base directory for all imports.

If the `start_directory` are not specified, `neatest` will find all the packages
inside the project directory and will run tests for each of them.

```
my_project
    package_a               # tests in package_a will be discovered
        __init__.py
    package_b               # tests in package_b will be discovered
        __init__.py
    package_c               # tests in package_c will be discovered
        __init__.py
        subpackage          # subpackage is a part of package_c 
            __init__.py     # so tests will be discovered
            ...
    subdir                  # subdir is not a package
        package_d           # tests in package_d will NOT be discovered  
            __init__.py     # because package_d is not importable    
  setup.py
```

So the commands

``` bash
$ cd my_project
$ neatest
```

will run the same tests as

``` bash
$ cd my_project
$ python3 -m unittest discover -t . -s package_a -p "*.py"
$ python3 -m unittest discover -t . -s package_b -p "*.py"
$ python3 -m unittest discover -t . -s package_c -p "*.py"
```


