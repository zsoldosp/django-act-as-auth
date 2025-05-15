from django.urls import path
from djactasauth.views import PrefillLoginView
from testapp.views import whoami


urlpatterns = [
    path(r'login/', PrefillLoginView.as_view(), {}, 'login'),
    path(r'whoami/', whoami),
]
