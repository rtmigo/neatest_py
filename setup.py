# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


from pathlib import Path

from setuptools import setup, find_packages

readme = (Path(__file__).parent / 'README.md').read_text()
import neatest.constants

setup(
    name="neatest",

    version=neatest.constants.__version__,

    author="Artёm IG",
    author_email="ortemeo@gmail.com",
    url='https://github.com/rtmigo/neatest_py',

    packages=find_packages(),
    install_requires=[],

    description='Runs tests with standard Python "unittest" module, '
                'but with modified discovery rules',

    long_description=readme,
    long_description_content_type='text/markdown',

    license='MIT',

    entry_points={
        'console_scripts': [
            'neatest = neatest:main_entry_point',
        ]},

    keywords="""unit tests unittest unit-tests testing discovery""".split(),

    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Documentation',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX",
    ],
)
