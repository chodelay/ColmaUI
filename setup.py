#!/usr/bin/python

from setuptools import setup
import sys

APP = ['ColmaUI.py']
DATA_FILES = []
OPTIONS = {}
sys.setrecursionlimit(15000)

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
