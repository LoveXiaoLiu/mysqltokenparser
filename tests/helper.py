import os, sys

path = sys.path
os.environ["PATH"] = os.path.abspath(
    os.path.join('../mysqltokenparser/', os.path.dirname(__file__))
)

from mysqltokenparser import mysqltokenparser
