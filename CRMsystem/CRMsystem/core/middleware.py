from django.http import HttpResponse


class FirstMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('We are in first middleware 1')
        response = self.get_response(request)
        print('We are in first middleware 2')
        return response

    def process_exception(self, request, exception):
        print('Exception is {exception}')
        return HttpResponse('Exception')


class SecondMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('We are in second middleware 1')
        response = self.get_response(request)
        print('We are in second middleware 2')
        return response
