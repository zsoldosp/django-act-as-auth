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

``djactasauth.backends.ActAsModelBackend``
..........................................

This is a subclass of ``FilteredModelBackend``.

You can have precise control over which user can act as which other kind
of user, by subclassing ``ActAsModelBackend``, and describing your policy
by overwriting the ``can_act_as(self, auth_user, user)`` method. For an
example, see ``djactasauth.backends.OnlySuperuserCanActAsModelBackend``.


``ActAsModelBackend`` by default doesn't allow anyone to act-as, so there
is no chance for misconfiguration.

``djactasauth.views.act_as_login_view``
.......................................

You can extend this through the standard ``kwargs``, as you would extend
``django.contrib.auth.views.login``, or you can create your own view
method that eventually delegates to it - the same way this implementation
does for django's own :-)

``djactasauth.views.get_login_form``
.....................................

This is used by ``djactasauth.views.act_as_login_view``. On the one hand,
it backports a django 1.6 feature to 1.5 (pass in ``request`` as an argument
to the form), and if needed, it mixes in
``djactasauth.forms.InitialValuesFromRequestGetFormMixin``, so the username
can be prefilled for act-as-auth links from the ``GET`` request.

``djactasauth.forms.InitialValuesFromRequestGetFormMixin``
..........................................................

It's a ``Form`` mixin, which - given one of its super`s has initialized
the form's ``self.request``, will got through ``self.request.GET``, and
copy over the values to ``self.initial`` - unless ``self.initial`` already
has a value for the given field names you declared in your class's 
``query2initial`` property (``tuple``).

This is needed for a feature here, but you might find it useful in other
parts of your code too :-)

``djactasauth.util.act_as_login_url``
.....................................

Convenience method to encapsulate how the act as auth username should be 
constructed from the two usernames.



Release Notes
-------------

* 0.1.3

  * explicitly add support for django 1.5 and 1.6

* 0.1.2

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
