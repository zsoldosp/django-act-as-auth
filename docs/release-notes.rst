Release Notes
=============

0.6.0
-----

   * version upgrade release
   * drop support for Django 1.11, 2.1, 2.2
   * add support for Django 4.2, 5.1, 5.2
   * drop support for Python 2.7, 3.5, 3.6, 3.7
   * add support for Python 3.9, 3.10, 3.11, 3.12, 3.13

0.3.0
-----

   * drop support for deprecated python and django versions
   * conform to latest flake8

0.2.1
-----

   * bugfix: #12 - won't crash if username contains multiple act as auth
     sepchars (e.g.: ``admin/user/`` (note the trailing slash)
   * bugfix: #13 - wrapping ``act_as_auth_view`` in ``sensitive_post_parameters``

0.2.0
-----

   * BACKWARDS INCOMPATIBLE: not inheriting from ``ModelBackend``,
     but rather working in addition to the existing
     ``settings.AUTHENTICATION_BACKENDS``
   * BACKWARDS INCOMPATIBLE: only one act-as-auth backend can be
     configured for ``settings.AUTHENTICATION_BACKENDS``

0.1.7
-----

  * add support for Django 1.11 and thus python 3.6

0.1.6
-----

  * add support for Django 1.10

0.1.5
-----

  * fix ``description`` on https://pypi.python.org

0.1.4
-----

  * first public release to pypi
  * fixed ``README.rst`` to look OK on https://pypi.python.org

0.1.3
-----

  * explicitly add support for Django 1.6 and 1.7
  * use Django's own bundled ``six`` instead of installing the external version
  * explicity add support for Django's own supported Python version, i.e.:
    Python 3.3 and 3.5 too (dropped 3.2 support as the travis build failed
    during setup)

0.1.2
-----

  * introduce

    * ``act_as_login_view``
    * ``act_as_login_url``
    * ``get_login_form``
    * ``InitialValuesFromRequestGetFormMixin``

    as part of the public api

  * "backport" to Django 1.5: ``authentication_form`` has ``request`` even
    on ``POST``
  * can prefill ``username`` from query string
  * bugfix: when user to act as is ``None``, don't crash the process (e.g.:
    when ``can_act_as`` checked some property of the user, thus generating
    an ``AttributeError``)

0.1.1
-----

  * bugfix: ``ActAsModelBackend.is_act_as_username`` used to fail when
    ``username`` argument was ``None``, now it returns ``False``
  * explicitly regression testing for login redirecting to
    value provided in ``REDIRECT_FIELD_NAME``
  * bugfix: ``setup.py`` now lists its dependencies (and added ``six``)

0.1.0
-----
  
  * initial release
  * supports Django 1.5, 1.8 and 1.9 on python 2.7 and 3.4
  * introduce ``FilteredModelBackend``, ``ActAsModelBackend``,
    and ``OnlySuperuserCanActAsModelBackend``
