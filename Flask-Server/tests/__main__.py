import sys,os

dirname = os.path.dirname(__file__)
srcdir = os.path.join(dirname, "src")
sys.path.insert(0,os.path.abspath(srcdir))

import server
