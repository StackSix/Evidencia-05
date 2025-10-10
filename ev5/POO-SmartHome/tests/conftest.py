import sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(ROOT, '..', 'src'))
PKG = os.path.join(SRC, 'smarthome')

for path in (SRC, PKG):
    if path not in sys.path:
        sys.path.insert(0, path)
