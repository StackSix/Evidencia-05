import sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(ROOT, '..', 'src'))
if SRC not in sys.path:
    sys.path.insert(0, SRC)
