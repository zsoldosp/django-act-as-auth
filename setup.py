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

description = \
    'Django authentication backend allowing admins to login as another user'

setup(
    name='djactasauth',
    description=description,
    version=version,
    author='Paessler AG',
    url='https://github.com/PaesslerAG/django-act-as-auth',
    packages=[
        'djactasauth',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.11.17,<2.0',
        'Django>=2.1.8,<2.2;python_version>"3.4"',
        'Django>=2.2.1,<2.3;python_version>"3.4"',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django, authentication, act as, impersonation',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
    ],
)
