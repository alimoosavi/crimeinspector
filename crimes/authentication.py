from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import NotAuthenticated
from django.conf import settings


class StaticTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_TOKEN", None)
        if not token or token != settings.AUTHENTICATION_STATIC_TOKEN:
            raise NotAuthenticated()
        return {}, None
