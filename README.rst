=============================
Django Act As Auth Backend
=============================

Django authentication that allows you to login as someone else

Quickstart
----------

Install djactasauth::

    pip install djactasauth

Add it to your auth backends in ``settings``::

    import djactasauth
    AUTHENTICATION_BACKENDS = (
        ...,
        'djactasauth.backends.OnlySuperuserCanActAsModelBackend',
        ...,
    )


Then you can log in with username ``your_superuser_name/customer`` and password
``yourpassword``.


Extension points
----------------

``FilteredModelBackend``
........................

If a subclass of ``FilteredModelBackend`` has a class or instance level
``filter_kwargs`` field, then those filters would be applied in the
``FilteredModelBackend.get_user`` method.

If there is no such field, it's ignored, and the behaviour is the same
as its parent, ``django.contrib.auth.backends.ModelBackend``.

An empty dictionary (``{}``) is also a valid value for filters, again,
the behavior is the same as if no such field was specifiec.

``ActAsModelBackend``
........................

This is a subclass of ``FilteredModelBackend``.

You can have precise control over which user can act as which other kind
of user, by subclassing ``ActAsModelBackend``, and describing your policy
by overwriting the ``can_act_as(self, auth_user, user)`` method. For an
example, see ``djactasauth.backends.OnlySuperuserCanActAsModelBackend``.


``ActAsModelBackend`` by default doesn't allow anyone to act-as, so there
is no chance for misconfiguration.

Release Notes
-------------

* 0.1.1

  * bugfix: ``ActAsModelBackend.is_act_as_username`` used to fail when
    ``username`` argument was ``None``, now it returns ``False``

* 0.1.0 - initial release

  * supports Django 1.5, 1.8 and 1.9 on python 2.7 and 3.4
  * introduce ``FilteredModelBackend``, ``ActAsModelBackend``,
    and ``OnlySuperuserCanActAsModelBackend``
