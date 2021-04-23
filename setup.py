# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


from pathlib import Path

from setuptools import setup, find_packages

readme = (Path(__file__).parent / 'README.md').read_text()

setup(
    name="neatest",
    version="0.0.1",

    author="Artёm IG",
    author_email="ortemeo@gmail.com",
    url='https://github.com/rtmigo/neatest_py',

    packages=find_packages(),
    install_requires=[],

    description="Runs standard unittest discovery and testing, requiring less rain dance.",

    long_description=readme,
    long_description_content_type='text/markdown',

    license='MIT',

    keywords="""unit test unittest unit-test testing discovery""".split(),

    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Documentation',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX",
    ],
)
