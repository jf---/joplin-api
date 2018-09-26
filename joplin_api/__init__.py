# coding: utf-8
"""
    This module allow us to manage our notes / folders / tags into our Joplin Editor
"""

from .core import JoplinApi

VERSION = (1, 0, 0)  # PEP 386
__version__ = ".".join([str(x) for x in VERSION])
