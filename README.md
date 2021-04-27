# [neatest](https://github.com/rtmigo/neatest_py)

Runs unit tests with standard Python `unittest` module.

Automates test discovery.

Can be conveniently invoked from Python code as `neatest.run(...)` method instead of
running `python -m unittest discover ...` in shell.

# Install

``` bash
pip3 install neatest
```

# Run

## Run tests from terminal

``` bash
$ cd my_project
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

It works well for the project layout like that:

```
my_project
    package_a
        __init__.py
        any_files.py
        can_contain.py
        tests_inside.py
        ...
    package_b
        __init__.py
        ...
    tests  
        __init__.py
        test_something.py
        test_anything.py
```

## Run tests from .py script

#### Create run_tests.py

``` python3
import neatest
neatest.run()
```

#### Run command

``` bash
$ cd my_project
$ python3 path/to/run_tests.py
```

The idea behind creating a script is to eliminate the need to create other
`.sh`, `.bat` or config files for the testing. All the information you need to
run tests is contained in single executable `.py` file. It is short and portable 
as the Python itself.

``` python3
import neatest
neatest.run(tests_require=['requests'],
            buffer=True,
            verbosity=neatest.Verbosity.verbose)
```

# Arguments

Most of the arguments to the `neatest.run(...)` method have the same names and
meanings as the arguments
of [unittest](https://docs.python.org/3/library/unittest.html#command-line-interface)
and [unittest discover](https://docs.python.org/3/library/unittest.html#test-discovery)
.

# Test discovery

The test discovery has different defaults than the
standard [unittest discover](https://docs.python.org/3/library/unittest.html#test-discovery)
. It may discover more `TestCase`s than the standard. 

## Filenames

`neatest` searches for tests in all `*.py` files.

The same can be achieved with standard `unittest` like this:

``` bash
$ python3 -m unittest discover -p "*.py"
```

## Directories

`neatest` assumes, that the current directory is the project directory. It
is the base directory for all imports.

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
            __init__.py     # because it is not importable    
  setup.py
```

So running

``` bash
$ cd my_project
$ neatest
```

will perform the same tests as

``` bash
$ cd my_project
$ python3 -m unittest discover -t . -s package_a -p "*.py"
$ python3 -m unittest discover -t . -s package_b -p "*.py"
$ python3 -m unittest discover -t . -s package_c -p "*.py"
```

For simple project structure it will work as well:

```
my_project
    __init__.py
    test_a.py       # tests from here will be discovered
    test_b.py       # tests from here will be discovered
    anything.py     # tests from here will be discovered
```