"""Encodes and decodes URLs.

__authors__ = "Gregory Gundersen"
__credits__ = "Ma'ayan Lab, Icahn School of Medicine at Mount Sinai"
__contact__ = "avi.maayan@mssm.edu"
"""


import urllib


def encode(url):
    pass


def decode(url):
    return urllib.unquote_plus(url)