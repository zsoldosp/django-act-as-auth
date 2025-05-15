from django.urls import reverse
import urllib.parse
from djactasauth.backends import ActAsBackend


def act_as_login_url(auth, act_as, **query):
    username = ActAsBackend.sepchar.join([auth, act_as])
    return get_login_url(username=username, **query)


def get_login_url(**query):
    return reverse('login') + '?' + urllib.parse.urlencode(query)
