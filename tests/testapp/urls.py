from django.conf.urls import url
from djactasauth.views import act_as_login_view
from testapp.views import whoami


urls = [
    url(r'^login/$', act_as_login_view, {}, 'login'),
    url(r'^whoami/$', whoami),
]
try:
    from django.conf.urls import patterns
    urlpatterns = patterns('testapp', *urls)
except ImportError:
    urlpatterns = urls
