from django.http import HttpResponse


class MyHttpResponse(HttpResponse):

    def __call__(self, request):
        if request.META['USER_COUNTRY'] == 'None':
            return self
        else:
            self.status_code = 403
