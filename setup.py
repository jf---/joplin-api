#!/usr/bin/env python
# coding: utf-8
import os
from setuptools import setup, find_packages

from joplin_api import __version__ as version


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(*f):
    return list(filter(None, [strip_comments(l) for l in open(
        os.path.join(os.getcwd(), *f)).readlines()]))


install_requires = reqs('requirements.txt')

setup(
    name='joplin-api',
    version=version,
    packages=find_packages(),
    author="FoxMaSk",
    author_email="foxmask at protonmail",
    description="Joplin Editor - API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important!
    url='https://github.com/foxmask/joplin-api',
    download_url="https://github.com/foxmask/joplin-api/archive/joplin_api-"
                 + version + ".zip",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Communications",
    ],
    include_package_data=True,
    install_requires=install_requires,
)
