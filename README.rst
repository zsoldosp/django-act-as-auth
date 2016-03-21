Django Act As Auth Backend
==========================

.. sales pitch start

Django authentication backend that allows one to login as someone else
(an existing Django user allowed to login) without having to know their
password.

Great for customer support and testing scenarios!

.. sales pitch end

.. image:: https://travis-ci.org/PaesslerAG/django-act-as-auth.svg?branch=master
        :target: https://travis-ci.org/PaesslerAG/django-act-as-auth

.. image:: https://readthedocs.org/projects/django-act-as-auth/badge/?version=latest
        :target: http://django-act-as-auth.readthedocs.org/

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

.. contributing start
Contributing
------------

As an open source project, we welcome contributions.

Reporting issues/improvements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please open an `issue on github <https://github.com/PaesslerAG/django-act-as-auth/issues/>`_
or provide a `pull request <https://github.com/PaesslerAG/django-act-as-auth/pulls/>`_
whether for code or for the documentation.

For non-trivial changes, we kindly ask you to open an issue, as it might be rejected.
However, if the diff of a pull request better illustrates the point, feel free to make
it a pull request anyway.

Pull Requests
~~~~~~~~~~~~~

* for code changes

  * it must have tests covering the change. You might be asked to cover missing scenarios
  * the latest ``flake8`` will be run and shouldn't produce any warning
  * if the change is significant enough, documentation has to be provided

* if you are not there already, add yourself to the `Authors <authors>`_ file

Setting up all Python versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    sudo apt-get -y install software-properties-common
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    for version in 3.2 3.3 3.5; do
      py=python$version
      sudo apt-get -y install ${py} ${py}-dev
    done

Code of Conduct
~~~~~~~~~~~~~~~

As it is a Django extension, it follows
`Django's own Code of Conduct <https://www.djangoproject.com/conduct/>`_.
As there is no mailing list yet, please just email one of the main authors
(see ``setup.py`` file)


.. contributing end
