import django
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm
from djactasauth.forms import InitialValuesFromRequestGetFormMixin


def act_as_login_view(request, **kwargs):
    base_form = kwargs.get('authentication_form', AuthenticationForm)
    if django.VERSION[:2] < (1, 6):
        class CaptureRequestActAsAuthForm(base_form):
            def __init__(self, *a, **kw):
                if request.method == 'POST':
                    kw.setdefault('request', request)  # "backport" from 1.6
                super(CaptureRequestActAsAuthForm, self).__init__(*a, **kw)

        base_form = CaptureRequestActAsAuthForm

    class InitialFromQueryAuthForm(
            InitialValuesFromRequestGetFormMixin, base_form):

        @property
        def query2initial(self):
            return super(InitialFromQueryAuthForm, self).query2initial + \
                    ('username',)

    return login(
        request, authentication_form=InitialFromQueryAuthForm, **kwargs)
