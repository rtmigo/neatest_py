# [neatest](https://github.com/rtmigo/neatest_py)
Runs standard Python unittest discovery and testing. Provides a more convenient way of configuring
the tests. 

It replaces the shell command `python -m unittest discover ...`  with a brief programmatic call from Python code.

# Why

Testing should be simple. One line command. A really short line.

`python -m unittest discover ...` is too long. 

`run_tests.sh` is better. But not pythonic and POSIX-only.

`run_tests.py` is much better.

For example, if your command looks like this

``` bash 
$ cd project_dir && python -m unittest discover -s ./mymodule -p '*.py' --buffer
```

you can replace it with `run_tests.py`:

``` python3
import neatest
neatest.pattern = "*.py"
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

neatest.pattern = '*.py'  # optional initialization

if __name__ == "__main__":
    neatest.run()
```

#### Terminal

``` bash
$ python3 run_tests.py
```


## Run tests with setup.py

#### project_dir / run_tests.py

``` python3
import neatest

neatest.pattern = '*.py'  # optional initialization
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

