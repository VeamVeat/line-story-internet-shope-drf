# from django.middleware.security
# from django.contrib.auth.middleware
# from django.middleware.csrf
# from django.contrib.sessions.middleware


class MyViewSetMixin:

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self.service_class(user=context.get('request').user))
        return context

    def get_serializer_class(self):
        assert hasattr(self, 'serializer_class_by_action'), 'Install serializer_class_by_action'

        return self.serializer_class_by_action.get(self.action, self.serializer_class)
