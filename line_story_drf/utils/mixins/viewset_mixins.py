
class MyViewSetMixin:

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self.service_class(user=context.get('request').user))
        return context

    def get_serializer_class(self):
        assert hasattr(self, 'serializer_class_by_action'), 'Install serializer_class_by_action'

        return self.serializer_class_by_action.get(self.action, self.serializer_class)


# class ProcessRequestMiddleware(MiddlewareMixin):
#     """
#     This middleware appends new payload in request body
#     """
#
#     def process_view(self, request, view_func, *view_args, **view_kwargs):
#         request_data = getattr(request, '_body', request.body)
#         request_data = json.loads(request_data)
#         # here you can write the logic to append the payload to request data
#         request._body = json.dumps(request_data)
#         return None