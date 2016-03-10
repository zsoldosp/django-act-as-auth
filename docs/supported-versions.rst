Supported Versions
==================

Version Numbers
---------------

The project is versioned in the spirit of `Semantic Versioning`_.
Note however that currently it's pre 1.0, thus `minor` version
changes can be backwards incompatible. I.e.: ``0.1.3`` and ``0.1.2``
are compatible, but ``0.2.0`` and ``0.1.3`` are not.

Django Versions
---------------

The project aims to support the versions Django itself supports.

Just because Django itself doesn't support a version doesn't mean
that the project will drop support for that. However, support for
these Django/Python versions can be dropped any time without prior
notice. Usually this would be because of a new Django relase that
would require bending over backwards to support older versions.

Supported version of djactasauth
--------------------------------

The project itself has only a single supported version, that is the latest
stable release.

I.e.: bugfixes are not backported, i.e.: if the current stable release is ``1.2.3``,
but the bug applies to all versions since ``0.1.2``, the bug will only be fixed in
``1.2.4``.

Supported Django and Python versions
------------------------------------

See ``tox.ini``.

.. include:: ../tox.ini
   :start-after: [tox]
   :end-before: [testenv]


.. _Semantic Versioning: http://semver.org/
