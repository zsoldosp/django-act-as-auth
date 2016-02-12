class InitialValuesFromRequestGetFormMixin(object):

    query2initial = tuple()

    def __init__(self, *a, **kw):
        super(InitialValuesFromRequestGetFormMixin, self).__init__(*a, **kw)
        field_names = set(self.query2initial)
        for field_name in field_names:
            val_from_query = self.request.GET.get(field_name, None)
            if val_from_query:
                self.initial.setdefault(field_name, val_from_query)
