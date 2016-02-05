from django.conf.urls import patterns, url
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm
from testapp.views import whoami


urlpatterns = patterns('testapp',
        url(r'^login/$', login, dict(authentication_form=AuthenticationForm)),
        url(r'^whoami/$', whoami),
)
