from assets.build import build
from assets.status import Statuses
import os
import sys


if __name__ == '__main__':
    if sys.argv[0]:
        if build():
            Statuses(1)

