from django.conf.urls import patterns, url
from djactasauth.views import act_as_login_view
from testapp.views import whoami


urlpatterns = patterns(
    'testapp',
    url(r'^login/$', act_as_login_view, {}, 'login'),
    url(r'^whoami/$', whoami),
)
