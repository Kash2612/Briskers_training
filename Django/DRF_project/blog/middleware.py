# blog/middleware.py

from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import BlacklistedToken  # Ensure this model exists

class BlacklistTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]  # Extract the token part

            try:
                access_token = AccessToken(token)

                # Check if the token is in the blacklist
                if BlacklistedToken.objects.filter(token=token).exists():
                    return JsonResponse(
                        {"detail": "This token has been blacklisted."},
                        status=401
                    )
            except (InvalidToken, TokenError):
                return JsonResponse(
                    {"detail": "Invalid or expired token."},
                    status=401
                )

        response = self.get_response(request)
        return response
