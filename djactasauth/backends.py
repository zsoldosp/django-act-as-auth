# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class FilteredModelBackend(ModelBackend):
    def get_user(self, user_id):
        user = super(FilteredModelBackend, self).get_user(user_id)
        return self.filter_user(user)

    def authenticate(self, username=None, password=None, **kwargs):
        user = super(FilteredModelBackend, self).authenticate(
                username=username, password=password, **kwargs)
        return self.filter_user(user)


    def filter_user(self, user):
        if not user:
            return user
        filters = getattr(self, 'filter_kwargs', None)
        if filters:
            qs = type(user)._default_manager.filter(pk=user.pk).filter(**filters)
            if not qs.exists():
                return None
        return user


class ActAsModelBackend(FilteredModelBackend):

    sepchar = '/'

    def authenticate(self, username=None, password=None, **kwargs):
        if self.sepchar in username:
            auth_username, act_as_username = username.split(self.sepchar)
        else:
            auth_username = act_as_username = username

        auth_user = super(ActAsModelBackend, self).authenticate(
                username=auth_username, password=password, **kwargs)
        if not auth_user:
            return auth_user
        if auth_username != act_as_username:
            UserModel = get_user_model()
            try:
                user = UserModel._default_manager.get_by_natural_key(act_as_username)
            except UserModel.DoesNotExist:
                user = None
            if not self.can_act_as(auth_user=auth_user, user=user):
                return None
        else:
            user = auth_user
        return user

    def can_act_as(self, auth_user, user):
        return False


class OnlySuperUserCanActAsModelBackend(ActAsModelBackend):
    def can_act_as(self, auth_user, user):
        return auth_user.is_superuser and not user.is_superuser
