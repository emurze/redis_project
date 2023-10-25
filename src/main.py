import sys

from dispather import dispatch


def run(*args):
    dispatch(*args)


if __name__ == '__main__':
    run(sys.argv[1:])
