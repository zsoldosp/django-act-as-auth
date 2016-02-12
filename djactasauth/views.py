import django
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm


def act_as_login_view(request, **kwargs):
    base_form = kwargs.get('authentication_form', AuthenticationForm)
    if django.VERSION[:2] < (1, 6):
        class CaptureRequestActAsAuthForm(base_form):
            def __init__(self, *a, **kw):
                if request.method == 'POST':
                    kw.setdefault('request', request)  # "backport" from 1.6
                return super(
                    CaptureRequestActAsAuthForm, self).__init__(*a, **kw)

        authentication_form = CaptureRequestActAsAuthForm
    else:
        authentication_form = base_form
    return login(request, authentication_form=authentication_form, **kwargs)
