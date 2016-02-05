from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.test import TransactionTestCase

from djactasauth.backends import FilteredModelBackend


class FilteredBackendTestCase(TransactionTestCase):

    def test_it_is_a_model_backend(self):
        self.assertTrue(
            issubclass(FilteredModelBackend, ModelBackend),
            FilteredModelBackend.__mro__)

    def test_can_declare_filters_which_apply_to_get_user(self):
        staff = User.objects.create(username='staff', is_staff=True, is_superuser=False)
        superuser = User.objects.create(username='superuser', is_staff=True, is_superuser=True)
        customer = User.objects.create(username='customer', is_staff=False, is_superuser=False)

        class TestFilteredBackend(FilteredModelBackend):

            def __init__(self, filter_kwargs):
                self.filter_kwargs = filter_kwargs

        def get_user(user, filter_kwargs):
            backend = TestFilteredBackend(filter_kwargs)
            return backend.get_user(user.pk)

        self.assertEqual(staff, get_user(staff, dict()))
        self.assertEqual(superuser, get_user(superuser, dict()))
        self.assertEqual(customer, get_user(customer, dict()))

        self.assertEqual(None, get_user(customer, dict(is_staff=True)))
        self.assertEqual(superuser, get_user(superuser, dict(is_superuser=True)))
        self.assertEqual(customer, get_user(customer, dict(username__startswith='c')))
        self.assertEqual(None, get_user(superuser, dict(username__startswith='c')))
