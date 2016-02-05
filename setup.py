#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import djactasauth

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = djactasauth.__version__

if sys.argv[-1] == 'publish':
    os.system('make release')
    sys.exit()

readme = open('README.rst').read()
description = 'Django authentication allowing admins to login as another user'

setup(
    name='djactasauth',
    version=version,
    description=description,
    long_description=readme,
    author='Paessler AG',
    url='https://github.com/PaesslerAG/django-act-as-auth',
    packages=[
        'djactasauth',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django, authentication, act as, impersonation',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
