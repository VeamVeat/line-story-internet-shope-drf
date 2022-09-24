
class MyViewSetMixin:

    def get_serializer_context(self):
        context = super().get_serializer_context()
        service_class = self._get_service_class(user=context.get('request').user)
        context.update(service_class)
        return context

    def get_serializer_class(self):
        assert hasattr(self, 'serializer_class_by_action'), 'Install serializer_class_by_action'

        return self.serializer_class_by_action.get(self.action, self.serializer_class)
