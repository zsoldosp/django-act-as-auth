from django.contrib.auth.views import login


def act_as_login_view(request, **kwargs):
    return login(request, **kwargs)
