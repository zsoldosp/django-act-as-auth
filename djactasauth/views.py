from django.contrib.auth.views import LoginView


class PrefillLoginView(LoginView):

    query2initial = ('username',)

    def get_initial(self):
        initial = super(PrefillLoginView, self).get_initial()
        field_names = set(self.query2initial)
        for field_name in field_names:
            val_from_query = self.request.GET.get(field_name, None)
            if val_from_query:
                initial.setdefault(field_name, val_from_query)
        return initial
