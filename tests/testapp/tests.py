from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth import signals as auth_signals
from django.contrib.auth.forms import AuthenticationForm
from django.test import TransactionTestCase
from django.test.utils import override_settings

from djactasauth.backends import FilteredModelBackend, ActAsModelBackend, OnlySuperUserCanActAsModelBackend


class FilteredBackendTestCase(TransactionTestCase):

    def test_it_is_a_model_backend(self):
        self.assertTrue(
            issubclass(FilteredModelBackend, ModelBackend),
            FilteredModelBackend.__mro__)

    def test_can_declare_filters_which_apply_to_get_user(self):
        staff = User.objects.create(username='staff', is_staff=True, is_superuser=False)
        superuser = User.objects.create(username='superuser', is_staff=True, is_superuser=True)
        customer = User.objects.create(username='customer', is_staff=False, is_superuser=False)
        for u in [staff, superuser, customer]:
            u.set_password('password')
            u.save()

        class TestFilteredBackend(FilteredModelBackend):

            def __init__(self, filter_kwargs):
                self.filter_kwargs = filter_kwargs

        def run_scenarios_with(test_method):
            self.assertEqual(staff, test_method(staff, dict()))
            self.assertEqual(superuser, test_method(superuser, dict()))
            self.assertEqual(customer, test_method(customer, dict()))

            self.assertEqual(None, test_method(customer, dict(is_staff=True)))
            self.assertEqual(superuser, test_method(superuser, dict(is_superuser=True)))
            self.assertEqual(customer, test_method(customer, dict(username__startswith='c')))
            self.assertEqual(None, test_method(superuser, dict(username__startswith='c')))

        def get_user(user, filter_kwargs):
            backend = TestFilteredBackend(filter_kwargs)
            return backend.get_user(user.pk)

        run_scenarios_with(get_user)

        def authenticate(user, filter_kwargs):
            backend = TestFilteredBackend(filter_kwargs)
            return backend.authenticate(username=user.username, password='password')

        run_scenarios_with(authenticate)


class ActAsModelBackendTestCase(TransactionTestCase):

    def test_it_is_a_filtered_model_backend(self):
        self.assertTrue(
            issubclass(ActAsModelBackend, FilteredModelBackend),
            ActAsModelBackend.__mro__)

    def test_can_authenticate_user(self):
        user = self.create_user(username='user', password='password')
        self.assertEqual(user, self.authenticate(username='user', password='password'))

    def test_can_become_another_user_with_own_password(self):
        admin = self.create_user(username='admin', password='admin password')
        user = self.create_user(username='user', password='user password')
        self.assertEqual(None, self.authenticate(username='admin/user', password='user password'))
        self.assertEqual(user, self.authenticate(username='admin/user', password='admin password'))

    def test_cannot_become_nonexistent_user(self):
        admin = self.create_user(username='admin', password='password')
        self.assertEqual(None, self.authenticate(username='admin/user', password='password'))

    def test_authenticate_does_not_fire_login_signal(self):
        def should_not_fire_login_signal(user, **kwargs):
            self.fail(
                'should not have fired login signal but did for %r' % user)

        admin = self.create_user(username='admin', password='admin password')
        user = self.create_user(username='user', password='user password')

        auth_signals.user_logged_in.connect(should_not_fire_login_signal)
        try:
            self.authenticate(username='admin/user', password='admin password')
        finally:
            auth_signals.user_logged_in.disconnect(should_not_fire_login_signal)
        self.assertEqual(user, self.authenticate(username='admin/user', password='admin password'))

    def test_regression_test_for_only_super_user_can_act_as_model_backend(self):

        admin1 = self.create_user(username='admin1', password='admin1 password', is_superuser=True)
        admin2 = self.create_user(username='admin2', password='admin2 password', is_superuser=True)
        user = self.create_user(username='user', password='user password', is_superuser=False)

        self.assertEqual(None, self.authenticate(username='user/admin1', password='user password', backend_cls=OnlySuperUserCanActAsModelBackend))
        self.assertEqual(None, self.authenticate(username='user/admin2', password='user password', backend_cls=OnlySuperUserCanActAsModelBackend))

        self.assertEqual(user, self.authenticate(username='admin1/user', password='admin1 password', backend_cls=OnlySuperUserCanActAsModelBackend))
        self.assertEqual(user, self.authenticate(username='admin2/user', password='admin2 password', backend_cls=OnlySuperUserCanActAsModelBackend))

        self.assertEqual(None, self.authenticate(username='admin1/admin2', password='admin1 password', backend_cls=OnlySuperUserCanActAsModelBackend))
        self.assertEqual(None, self.authenticate(username='admin2/admin1', password='admin2 password', backend_cls=OnlySuperUserCanActAsModelBackend))

    def test_can_customize_can_act_as_policy_by_subclassing(self):
        alice = self.create_user(username='alice', password='alice')
        bob = self.create_user(username='bob', password='bob')

        class OnlyShortUserNamesCanActAs(ActAsModelBackend):

            def can_act_as(self, auth_user, user):
                return len(auth_user.username) <= 3

        self.assertEqual(None, self.authenticate(username='alice/bob', password='alice', backend_cls=OnlyShortUserNamesCanActAs))
        self.assertEqual(alice, self.authenticate(username='bob/alice', password='bob', backend_cls=OnlyShortUserNamesCanActAs))

###

    def create_user(self, username, password, is_superuser=False):
        user = User(username=username, is_superuser=is_superuser)
        user.set_password(password)
        user.save()
        return user

    def authenticate(self, username, password, backend_cls=None):
        if not backend_cls:
            class EveryoneCanActAs(ActAsModelBackend):
                def can_act_as(self, auth_user, user):
                    return True
            backend_cls = EveryoneCanActAs

        return backend_cls().authenticate(username=username, password=password)


@override_settings(AUTHENTICATION_BACKENDS=['djactasauth.backends.OnlySuperuserCanActAsModelBackend'])
class EndToEndActAsThroughFormAndView(TransactionTestCase):

    def test_login_page_is_set_up_as_expected(self):
        response = self.client.get('/login/')
        self.assertEquals(200, response.status_code)
        form = response.context['form']
        self.assertEquals(AuthenticationForm, type(form))
