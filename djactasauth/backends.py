# -*- coding: utf-8 -*-
import django
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

_authenticate_needs_request_arg = django.VERSION[:2] >= (1, 11)


class FilteredModelBackend(ModelBackend):
    def get_user(self, user_id):
        user = super(FilteredModelBackend, self).get_user(user_id)
        return self.filter_user(user)

    if _authenticate_needs_request_arg:
        def authenticate(self,
                         request, username=None, password=None, **kwargs):
            return self._authenticate(
                request=request, username=username, password=password,
                **kwargs)
    else:
        def authenticate(self, username=None, password=None, **kwargs):
            return self._authenticate(
                username=username, password=password, **kwargs)

    def _authenticate(self, **kwargs):
            user = super(FilteredModelBackend, self).authenticate(**kwargs)
            return self.filter_user(user)

    def filter_user(self, user):
        if not user:
            return user
        filters = getattr(self, 'filter_kwargs', None)
        if filters:
            qs = type(user)._default_manager.filter(
                pk=user.pk).filter(**filters)
            if not qs.exists():
                return None
        return user


class ActAsBackend(object):

    sepchar = '/'

    @classmethod
    def is_act_as_username(cls, username):
        if not username:
            return False
        return cls.sepchar in username

    if _authenticate_needs_request_arg:
        def authenticate(self,
                         request, username=None, password=None, **kwargs):
            return self._authenticate(
                request=request, username=username, password=password,
                **kwargs)
    else:
        def authenticate(self, username=None, password=None, **kwargs):
            return self._authenticate(
                username=username, password=password, **kwargs)

    def _authenticate(self, username=None, password=None, **kwargs):
        assert password is not None
        from django.contrib.auth import get_backends
        if not self.is_act_as_username(username):
            return None
        for backend in get_backends():
            if not isinstance(backend, ActAsBackend):
                auth_username, act_as_username = username.split(self.sepchar)
                auth_user = backend.authenticate(
                    username=auth_username, password=password, **kwargs)
                if auth_user:
                    return self.get_act_as_user(
                        auth_user=auth_user, act_as_username=act_as_username)

    def get_act_as_user(self, auth_user, act_as_username):
        if auth_user.username != act_as_username:
            UserModel = get_user_model()
            try:
                user = self._get_user_manager().get_by_natural_key(
                    act_as_username)
            except UserModel.DoesNotExist:
                return None
            if not self.can_act_as(auth_user=auth_user, user=user):
                return None
        else:
            user = auth_user
        return user

    def _get_user_manager(self):
        UserModel = get_user_model()
        return UserModel._default_manager

    def can_act_as(self, auth_user, user):
        return False

    def get_user(self, user_id):
        return self._get_user_manager().get(pk=user_id)


class OnlySuperuserCanActAsBackend(ActAsBackend):
    def can_act_as(self, auth_user, user):
        return auth_user.is_superuser and not user.is_superuser
