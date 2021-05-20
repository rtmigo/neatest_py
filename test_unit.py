import sys
from subprocess import check_call

if __name__ == "__main__":
    check_call([sys.executable] + "-m unittest discover -t . -s tests".split())
