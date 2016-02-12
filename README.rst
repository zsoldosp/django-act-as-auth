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

Configure the custom login view to take advantage of all the features
in your ``urls.py``::

    from django.conf.urls import patterns, url
    from djactasauth.views import act_as_login_view
    from testapp.views import whoami


    urlpatterns = patterns(
        '',
        url(r'^login/$', act_as_login_view, {}, 'login'),
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
.....................

This is a subclass of ``FilteredModelBackend``.

You can have precise control over which user can act as which other kind
of user, by subclassing ``ActAsModelBackend``, and describing your policy
by overwriting the ``can_act_as(self, auth_user, user)`` method. For an
example, see ``djactasauth.backends.OnlySuperuserCanActAsModelBackend``.


``ActAsModelBackend`` by default doesn't allow anyone to act-as, so there
is no chance for misconfiguration.

``act_as_login_view``
.....................

You can extend this through the standard ``kwargs``, as you would extend
``django.contrib.auth.views.login``, or you can create your own view
method that eventually delegates to it - the same way this implementation
does for django's own :-)

Release Notes
-------------

* 0.1.2

  * introduce ``act_as_login_view``

* 0.1.1

  * bugfix: ``ActAsModelBackend.is_act_as_username`` used to fail when
    ``username`` argument was ``None``, now it returns ``False``
  * explicitly regression testing for login redirecting to
    value provided in ``REDIRECT_FIELD_NAME``
  * bugfix: ``setup.py`` now lists its dependencies (and added ``six``)

* 0.1.0 - initial release

  * supports Django 1.5, 1.8 and 1.9 on python 2.7 and 3.4
  * introduce ``FilteredModelBackend``, ``ActAsModelBackend``,
    and ``OnlySuperuserCanActAsModelBackend``
