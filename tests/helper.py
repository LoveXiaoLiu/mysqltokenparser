import os
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join('../mysqltokenparser/', os.path.dirname(__file__))
))

from mysqltokenparser import mysqltokenparser
from mysqltokenparser import constant
