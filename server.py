import os
import sys

from bolinette.cli import Parser
from example import bolinette

if __name__ == '__main__':
    cwd = os.getcwd()
    Parser(cwd, bolinette).execute(sys.argv)
