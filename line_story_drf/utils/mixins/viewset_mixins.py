

class ViewSetMixin:

    def get_serializer_class(self):
        assert hasattr(self, 'serializer_class_by_action'), 'Install serializer_class_by_action'

        return self.serializer_class_by_action.get(self.action, self.serializer_class)

