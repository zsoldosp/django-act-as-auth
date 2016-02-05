from django.conf.urls import patterns, url
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm


urlpatterns = patterns('testapp',
        url(r'^login/$', login, dict(authentication_form=AuthenticationForm)),
)
