import django
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.debug import sensitive_post_parameters
from djactasauth.forms import InitialValuesFromRequestGetFormMixin


def get_login_form(request, authentication_form=AuthenticationForm, **kwargs):
    base_form = authentication_form
    if django.VERSION[:2] < (1, 6):
        class CaptureRequestActAsAuthForm(base_form):
            def __init__(self, *a, **kw):
                if request.method == 'POST':
                    kw.setdefault('request', request)  # "backport" from 1.6
                super(CaptureRequestActAsAuthForm, self).__init__(*a, **kw)

        base_form = CaptureRequestActAsAuthForm

    if not issubclass(base_form, InitialValuesFromRequestGetFormMixin):
        class InitialFromQueryAuthForm(
                InitialValuesFromRequestGetFormMixin, base_form):

            @property
            def query2initial(self):
                return super(InitialFromQueryAuthForm, self).query2initial + \
                        ('username',)

        base_form = InitialFromQueryAuthForm
    else:
        # TODO: raise warning if it doesn't have username in query2initial
        pass

    return base_form


@sensitive_post_parameters('password')
def act_as_login_view(request, **kwargs):
    # in-mehod import otherwise cannot mock it due to sensitive wraps
    # see test_act_as_login_view_protects_sensitive_vars
    from django.contrib.auth.views import login
    kwargs['authentication_form'] = get_login_form(request, **kwargs)
    return login(request, **kwargs)
