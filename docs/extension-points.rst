Extension points
================

Authentication Backends
-----------------------

FilteredModelBackend
....................

If a subclass of ``djactasauth.backends.FilteredModelBackend`` has a class
or instance level ``filter_kwargs`` field, then those filters would be applied
in the ``FilteredModelBackend.get_user`` method.

If there is no such field, it's ignored, and the behaviour is the same
as its parent, ``django.contrib.auth.backends.ModelBackend``.

An empty dictionary (``{}``) is also a valid value for filters, again,
the behavior is the same as if no such field was specifiec.

``ActAsModelBackend``
.....................

This is a subclass of ``djactasauth.backends.FilteredModelBackend``.

You can have precise control over which user can act as which other kind
of user, by subclassing ``djactasauth.backends.ActAsModelBackend``, and describing your policy
by overwriting the ``can_act_as(self, auth_user, user)`` method. For an
example, see ``djactasauth.backends.OnlySuperuserCanActAsModelBackend``.

``ActAsModelBackend`` by default doesn't allow anyone to act-as, so there
is no chance for misconfiguration.


Views
-----

``act_as_login_view``
.....................


You can extend ``djactasauth.views.act_as_login_view`` through the
standard ``kwargs``, as you would extend
``django.contrib.auth.views.login``, or you can create your own view
method that eventually delegates to it - the same way this implementation
does for django's own :-)

Forms
-----

``get_login_form``
..................

``djactasauth.views.get_login_form``

This is used by ``djactasauth.views.act_as_login_view``. On the one hand,
it backports a django 1.6 feature to 1.5 (pass in ``request`` as an argument
to the form), and if needed, it mixes in
``djactasauth.forms.InitialValuesFromRequestGetFormMixin``, so the username
can be prefilled for act-as-auth links from the ``GET`` request.

``InitialValuesFromRequestGetFormMixin``
........................................

``djactasauth.forms.InitialValuesFromRequestGetFormMixin`` is a
``Form`` mixin, which - given one of its super`s has initialized
the form's ``self.request``, will got through ``self.request.GET``, and
copy over the values to ``self.initial`` - unless ``self.initial`` already
has a value for the given field names you declared in your class's 
``query2initial`` property (``tuple``).

This is needed for a feature here, but you might find it useful in other
parts of your code too :-)

Other
-----

``djactasauth.util.act_as_login_url``
.....................................

Convenience method to encapsulate how the act as auth username should be
constructed from the two usernames.
