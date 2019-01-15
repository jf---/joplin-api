# coding: utf-8
"""
    This module allow us to manage our notes / folders /
    tags into our Joplin Editor
"""

from .core import JoplinApi

from pkg_resources import get_distribution
__version__ = get_distribution('joplin_api').version
