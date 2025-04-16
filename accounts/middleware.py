
from django.http import HttpResponseForbidden

ALLOWED_IPS = ['127.0.0.1', ]

class RestrictApiAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api-auth/'):
            ip = request.META.get('REMOTE_ADDR')
            if ip not in ALLOWED_IPS:
                return HttpResponseForbidden("You are not authorized to access this resource.")

        response = self.get_response(request)
        return response