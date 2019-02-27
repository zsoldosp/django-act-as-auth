from django.conf.urls import url
from djactasauth.views import PrefillLoginView
from testapp.views import whoami
import django


urls = [
    url(r'^login/$', PrefillLoginView.as_view(), {}, 'login'),
    url(r'^whoami/$', whoami),
]
if django.VERSION[:2] < (1, 8):
    from django.conf.urls import patterns
    urlpatterns = patterns('testapp', *urls)
else:
    urlpatterns = urls
