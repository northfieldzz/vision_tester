import sys
from os import path
from logging import getLogger

logger = getLogger(__name__)

if getattr(sys, 'frozen', False):
    ROOT = path.dirname(sys.executable)
else:
    ROOT = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

STATIC_DIR = path.join(ROOT, 'static')
