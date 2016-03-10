Django Act As Auth Backend
==========================

.. sales pitch start

Django authentication backend that allows one to login as someone else, 
without having to know their passwords.

Great for customer support and testing scenarios!

.. sales pitch end

.. quickstart start

Quickstart
----------

Install ``djactasauth``::

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

.. quickstart end
