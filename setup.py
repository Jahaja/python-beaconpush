#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='python-beaconpush',
    version='0.1',
    description='A straight-forward python client for the BeaconPush API (http://beaconpush.com)',
    author='Joakim Hamrén',
    author_email='joakim.hamren@esn.me',
    url='http://beaconpush.com/',
    package_dir={'': 'src'},
    py_modules=[
        'beaconpush',
    ],
)