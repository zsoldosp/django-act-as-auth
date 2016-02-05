# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend


class FilteredModelBackend(ModelBackend):
    def get_user(self, user_id):
        user = super(FilteredModelBackend, self).get_user(user_id)
        if not user:
            return user
        filters = getattr(self, 'filter_kwargs', None)
        if filters:
            qs = type(user)._default_manager.filter(pk=user.pk).filter(**filters)
            if not qs.exists():
                return None
        return user
