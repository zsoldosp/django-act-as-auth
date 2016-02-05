=============================
djactasauth
=============================

Django authentication that allows you to login as someone else

Quickstart
----------

Install djactasauth::

    pip install django-act-as-auth

Add it to your auth backends in ``settings``::

    import djactasauth
    AUTHENTICATION_BACKENDS = (
        ...,
        'djactasauth.backends.ActAsModelBackend',
        ...,
    )

Then you can log in with username ``yourusername/customer`` and password
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



Release Notes
-------------

* 0.1.0 - initial release

  * supports Django 1.5 and 1.8 on python 2.7
  * introduce ``FilteredModelBackend``
