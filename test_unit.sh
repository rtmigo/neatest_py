#!/bin/bash
set -e

python3 -m unittest discover -t . -s tests

