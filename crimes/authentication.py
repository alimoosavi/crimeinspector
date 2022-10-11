from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings


# class CrimeListAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         token = request.META.get("Token", None)
#         if not token or token != settings.AUTHENTICATION_STATIC_TOKEN:
#             raise exceptions.AuthenticationFailed('AUTHENTICATION TOKEN IS NOT VALID')
#
#         return (None, None,)
