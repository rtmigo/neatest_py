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
Module "module_a" contains 3 tests
Module "module_b" contains 4 tests
Module "tests" contains 16 tests
.....
----------------------------------------------------------------------
Ran 23 tests in 2.947s

OK
```

It works well for the project layout like that:

```
my_project
    module_a
        __init__.py
        any_files.py
        can_contain.py
        tests_inside.py
        ...
    module_b
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

`neatest` assumes, that the current directory is the `top_level_directory`. It
is the base directory for all imports.

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
    submodule           # submodule will be tested as a part of module_c 
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

