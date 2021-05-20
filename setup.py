# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


from pathlib import Path
from typing import Any, Dict

from setuptools import setup


def load_module_dict(filename: str) -> Dict[str, Any]:
    import importlib.util as ilu
    filename = str(Path(__file__).parent / filename)
    spec = ilu.spec_from_file_location('', filename)
    module = ilu.module_from_spec(spec)
    # noinspection Mypy
    spec.loader.exec_module(module)
    return module.__dict__


readme = (Path(__file__).parent / 'README.md').read_text()
name = "neatest"
constants = load_module_dict(f'{name}/_constants.py')

setup(
    name=name,

    version=constants['__version__'],

    author="Artёm IG",
    author_email="ortemeo@gmail.com",
    url='https://github.com/rtmigo/neatest_py#neatest',

    packages=['neatest'],
    install_requires=[],
    python_requires='>=3.7',

    description='Discovers and runs unit tests with a single-word command.',

    long_description=readme,
    long_description_content_type='text/markdown',

    license='MIT',

    entry_points={
        'console_scripts': [
            'neatest = neatest:main_entry_point',
        ]},

    keywords="""unit tests unittest unit-tests 
                testing discovery test ci""".split(),

    # https://pypi.org/classifiers/
    classifiers=[
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Unit',
        'Topic :: Software Development :: Quality Assurance',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX",
        'Operating System :: Microsoft :: Windows'
    ],

)
