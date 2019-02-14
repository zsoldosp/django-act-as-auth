# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.backends import ModelBackend
from django.contrib import auth

log = logging.getLogger(__name__)


class FilteredModelBackend(ModelBackend):
    def get_user(self, user_id):
        user = super(FilteredModelBackend, self).get_user(user_id)
        return self.filter_user(user)

    def authenticate(self, request, **kwargs):
        user = super(FilteredModelBackend, self).authenticate(
            request=request, **kwargs)
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
    too_many_sepchar_msg = 'Username holds more than one separation char "{}"'\
        '.'.format(sepchar)

    @classmethod
    def is_act_as_username(cls, username):
        if not username:
            return False
        if username.count(ActAsBackend.sepchar) > 1:
            log.warn(cls.too_many_sepchar_msg)
            return False
        return cls.sepchar in username

    def authenticate(self, request, username=None, password=None, **kwargs):
        self.fail_unless_one_aaa_backend_is_configured()
        assert password is not None
        if not self.is_act_as_username(username):
            return None
        auth_username, act_as_username = username.split(self.sepchar)
        backends = [b for b in auth.get_backends() if not
                    isinstance(b, ActAsBackend)]
        for backend in backends:
            auth_user = backend.authenticate(
                request=request, username=auth_username, password=password,
                **kwargs)
            if auth_user:
                return self.get_act_as_user(
                    auth_user=auth_user, act_as_username=act_as_username)

    def fail_unless_one_aaa_backend_is_configured(self):
        aaa_backends = list(
            type(backend) for backend in auth.get_backends()
            if isinstance(backend, ActAsBackend))
        if len(aaa_backends) != 1:
            raise ValueError(
                'There should be exactly one AAA backend configured, '
                'but there were {}'.format(aaa_backends))

    def get_act_as_user(self, auth_user, act_as_username):
        if auth_user.username != act_as_username:
            UserModel = auth.get_user_model()
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
        UserModel = auth.get_user_model()
        return UserModel._default_manager

    def can_act_as(self, auth_user, user):
        return False

    def get_user(self, user_id):
        return self._get_user_manager().get(pk=user_id)


class OnlySuperuserCanActAsBackend(ActAsBackend):
    def can_act_as(self, auth_user, user):
        return auth_user.is_superuser and not user.is_superuser
