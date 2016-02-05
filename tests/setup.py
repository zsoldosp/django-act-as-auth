#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] in ('publish', 'release'):
    raise Exception('this is a test app, do not release it!')

readme = 'A simple test application to test djactasauth'

setup(
    name='testapp',
    version='0.0.0',
    description=readme,
    long_description=readme,
    author='Paessler AG',
    url='https://github.com/PaesslerAG/django-act-as-auth',
    packages=[
        'testapp',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-act-as-auth',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
