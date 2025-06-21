from django.http import JsonResponse
from django.conf import settings

class AccessKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.expected_key = getattr(settings, "SERVER_ACCESS_KEY", None)

    def __call__(self, request):
        access_key = request.headers.get("X-Access-Key")

        if self.expected_key and access_key != self.expected_key:
            return JsonResponse(data={
                "detail": "Access key invalid."
            }, status=401)

        return self.get_response(request)
