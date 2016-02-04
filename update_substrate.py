#!/usr/bin/env python

"""Utility script for remember the command to update Substrate from GitHub.
"""

import argparse
import subprocess


ap = argparse.ArgumentParser()
ap.add_argument('--branch',
                help='branch from which to pull',
                default='master')
opts = ap.parse_args()
print(opts)

cmd = 'sudo pip install --upgrade --no-deps --force-reinstall git+git://' \
      'github.com/MaayanLab/substrate.git@%s' % opts.branch
print(cmd)
subprocess.call(cmd, shell=True)
