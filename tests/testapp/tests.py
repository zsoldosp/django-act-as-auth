from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.test import TransactionTestCase

from djactasauth.backends import FilteredModelBackend, ActAsModelBackend


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
        self.assertEqual(user, ActAsModelBackend().authenticate(username='user', password='password'))

    def test_can_become_another_user_with_own_password(self):
        admin = self.create_user(username='admin', password='admin password')
        user = self.create_user(username='user', password='user password')
        self.assertEqual(None, ActAsModelBackend().authenticate(username='admin/user', password='user password'))
        self.assertEqual(user, ActAsModelBackend().authenticate(username='admin/user', password='admin password'))

    def test_cannot_become_nonexistent_user(self):
        admin = self.create_user(username='admin', password='password')
        self.assertEqual(None, ActAsModelBackend().authenticate(username='admin/user', password='password'))


###

    def create_user(self, username, password):
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user
