import django
from django.utils.six.moves.urllib import parse
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth import signals as auth_signals, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.test import TransactionTestCase
from django.test.utils import override_settings

from djactasauth.backends import \
    FilteredModelBackend, ActAsModelBackend, OnlySuperuserCanActAsModelBackend
from djactasauth.util import act_as_login_url, get_login_url


def create_user(
        username, password='password', is_superuser=False, is_staff=False):
    user = User(username=username, is_superuser=is_superuser)
    user.set_password(password)
    user.save()
    return user


def auth_through_backend(backend, **kwargs):
    if django.VERSION[:2] >= (1, 11):
        args = [None]  # request
    else:
        args = []
    return backend.authenticate(*args, **kwargs)


class FilteredBackendTestCase(TransactionTestCase):

    def test_it_is_a_model_backend(self):
        self.assertTrue(
            issubclass(FilteredModelBackend, ModelBackend),
            FilteredModelBackend.__mro__)

    def test_can_declare_filters_which_apply_to_get_user(self):
        staff = create_user(
            username='staff', is_staff=True, is_superuser=False)
        superuser = create_user(
            username='superuser', is_staff=True, is_superuser=True)
        customer = create_user(
            username='customer', is_staff=False, is_superuser=False)
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
            self.assertEqual(
                superuser, test_method(superuser, dict(is_superuser=True)))
            self.assertEqual(
                customer, test_method(
                    customer, dict(username__startswith='c')))
            self.assertEqual(
                None, test_method(superuser, dict(username__startswith='c')))

        def get_user(user, filter_kwargs):
            backend = TestFilteredBackend(filter_kwargs)
            return backend.get_user(user.pk)

        run_scenarios_with(get_user)

        def authenticate(user, filter_kwargs):
            backend = TestFilteredBackend(filter_kwargs)
            return auth_through_backend(
                backend=backend, username=user.username, password='password')

        run_scenarios_with(authenticate)


class ActAsModelBackendTestCase(TransactionTestCase):

    def test_it_is_a_filtered_model_backend(self):
        self.assertTrue(
            issubclass(ActAsModelBackend, FilteredModelBackend),
            ActAsModelBackend.__mro__)

    def test_can_authenticate_user(self):
        user = create_user(username='user', password='password')
        self.assertEqual(
            user, self.authenticate(username='user', password='password'))

    def test_can_become_another_user_with_own_password(self):
        create_user(username='admin', password='admin password')
        user = create_user(username='user', password='user password')
        self.assertEqual(
            None, self.authenticate(
                username='admin/user', password='user password'))
        self.assertEqual(
            user, self.authenticate(
                username='admin/user', password='admin password'))

    def test_cannot_become_nonexistent_user(self):
        create_user(username='admin', password='password')
        self.assertEqual(
            None, self.authenticate(
                username='admin/user', password='password'))

    def test_authenticate_does_not_fire_login_signal(self):
        def should_not_fire_login_signal(user, **kwargs):
            self.fail(
                'should not have fired login signal but did for %r' % user)

        create_user(username='admin', password='admin password')
        user = create_user(username='user', password='user password')

        auth_signals.user_logged_in.connect(should_not_fire_login_signal)
        try:
            self.authenticate(username='admin/user', password='admin password')
        finally:
            auth_signals.user_logged_in.disconnect(
                should_not_fire_login_signal)
        self.assertEqual(
            user, self.authenticate(
                username='admin/user', password='admin password'))

    def test_only_super_user_can_act_as_model_backend_regression(self):
        create_user(
            username='admin1', password='admin1 password', is_superuser=True)
        create_user(
            username='admin2', password='admin2 password', is_superuser=True)
        user = create_user(
            username='user', password='user password', is_superuser=False)

        self.assertEqual(
            None, self.authenticate(
                username='user/admin1', password='user password',
                backend_cls=OnlySuperuserCanActAsModelBackend))
        self.assertEqual(
            None, self.authenticate(
                username='user/admin2', password='user password',
                backend_cls=OnlySuperuserCanActAsModelBackend))

        self.assertEqual(
            user, self.authenticate(
                backend_cls=OnlySuperuserCanActAsModelBackend,
                username='admin1/user', password='admin1 password'))
        self.assertEqual(
            user, self.authenticate(
                backend_cls=OnlySuperuserCanActAsModelBackend,
                username='admin2/user', password='admin2 password'))

        self.assertEqual(
            None, self.authenticate(
                backend_cls=OnlySuperuserCanActAsModelBackend,
                username='admin1/admin2', password='admin1 password'))
        self.assertEqual(
            None, self.authenticate(
                backend_cls=OnlySuperuserCanActAsModelBackend,
                username='admin2/admin1', password='admin2 password'))

    def test_can_customize_can_act_as_policy_by_subclassing(self):
        alice = create_user(username='alice', password='alice')
        create_user(username='bob', password='bob')

        class OnlyShortUserNamesCanActAs(ActAsModelBackend):

            def can_act_as(self, auth_user, user):
                return len(auth_user.username) <= 3

        self.assertEqual(
            None, self.authenticate(
                backend_cls=OnlyShortUserNamesCanActAs,
                username='alice/bob', password='alice'))
        self.assertEqual(
            alice, self.authenticate(
                backend_cls=OnlyShortUserNamesCanActAs,
                username='bob/alice', password='bob'))

    def test_when_users_none_doesnt_crash_process(self):
        create_user(username='jane', password='doe')

        class ShouldNotCallCanActAs(ActAsModelBackend):

            def can_act_as(backend_self, auth_user, user):
                self.fail('should not have called')

        self.assertEqual(
            None, self.authenticate(
                backend_cls=ShouldNotCallCanActAs,
                username='jane/non-existent-user', password='doe'))

    def test_is_act_as_username_method(self):
        def assert_classification(username, expected_to_be_act_as_username):
            self.assertEqual(
                expected_to_be_act_as_username,
                ActAsModelBackend.is_act_as_username(username))

        assert_classification(None, False)
        assert_classification('', False)
        assert_classification('user', False)
        assert_classification('user/johndoe', True)

###

    def authenticate(self, username, password, backend_cls=None):
        if not backend_cls:
            class EveryoneCanActAs(ActAsModelBackend):
                def can_act_as(self, auth_user, user):
                    return True
            backend_cls = EveryoneCanActAs

        return auth_through_backend(
            backend_cls(), username=username, password=password)


@override_settings(
    AUTHENTICATION_BACKENDS=[
        'djactasauth.backends.OnlySuperuserCanActAsModelBackend'])
class EndToEndActAsThroughFormAndView(TransactionTestCase):

    def test_login_page_is_set_up_as_expected(self):
        self.goto_login_page()
        response = self.login_get_response
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertTrue(
            isinstance(form, AuthenticationForm), type(form).__mro__)

    def test_successful_act_as_login_fires_signal_with_act_as_user(self):
        logged_in_users = []

        def handle_user_logged_in(user, **kwargs):
            logged_in_users.append(user)

        auth_signals.user_logged_in.connect(handle_user_logged_in)
        create_user(username='admin', password='admin', is_superuser=True)
        user = create_user(
            username='user', password='user', is_superuser=False)
        try:
            self.goto_login_page()
            self.submit_login(username='admin/user', password='admin')
            self.assertEqual(302, self.login_post_response.status_code)
        finally:
            auth_signals.user_logged_in.disconnect(handle_user_logged_in)
        self.assertEqual([user], logged_in_users)

    def test_after_login_correct_user_is_passed_in_the_request_no_act_as(self):
        create_user(username='admin', password='admin', is_superuser=True)
        self.assert_logged_in_user_on_next_request(
            username='admin', password='admin', display_user='admin')

    def test_after_login_correct_user_is_passed_in_the_request_act_as(self):
        create_user(username='admin', password='admin', is_superuser=True)
        create_user(username='user', password='user', is_superuser=False)
        self.assert_logged_in_user_on_next_request(
            username='admin/user', password='admin', display_user='user')

    def test_next_from_GET_is_respected_and_user_is_redirected_there(self):
        create_user(username='user', password='user', is_superuser=False)
        self.assert_logged_in_user_on_next_request(
            username='user', password='user', display_user='user',
            **{REDIRECT_FIELD_NAME: '/foo/'})
        redir_to = parse.urlparse(self.login_post_response['Location'])
        self.assertEqual('/foo/', redir_to.path)

    def test_on_post_form_has_access_to_request(self):
        self.goto_login_page()
        self.submit_login(username='foo', password='bar')
        response = self.login_post_response
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertTrue(hasattr(form, 'request'))
        self.assertIsNotNone(form.request)

    def test_can_initialize_username_from_querystring(self):
        self.goto_login_page(username='foo')
        form = self.login_get_response.context['form']
        self.assertEqual('foo', form.initial.get('username'))

###

    def assert_logged_in_user_on_next_request(
            self, username, password, display_user, **query):

        self.goto_login_page(**query)

        self.submit_login(username=username, password=password, **query)
        self.assertEqual(302, self.login_post_response.status_code)

        self.get_whoami_page()
        self.assertEqual(
            display_user, self.whoami_response.content.decode('ascii'))

    def goto_login_page(self, **query):
        url = get_login_url(**query)
        self.login_get_response = self.client.get(url)
        self.assertEqual(200, self.login_get_response.status_code)

    def submit_login(self, username, password, **query):
        url = get_login_url(**query)
        self.login_post_response = self.client.post(
            url, dict(username=username, password=password))

    def get_whoami_page(self):
        self.whoami_response = self.client.get('/whoami/')
        self.assertEqual(200, self.whoami_response.status_code)


class ActAsUrlGeneratorTestCase(TransactionTestCase):

    def test_generates_the_correct_url(self):
        self.assertEqual(
            '/login/?username=admin%2Fuser',
            act_as_login_url(auth='admin', act_as='user'))

        self.assertEqual(
            '/login/?username=foo%2Fbar',
            act_as_login_url(auth='foo', act_as='bar'))
