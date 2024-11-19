# utils.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import BlacklistedToken
from rest_framework.exceptions import AuthenticationFailed

def check_blacklist(token):
    """Check if the token is blacklisted"""
    if BlacklistedToken.objects.filter(token=token).exists():
        raise AuthenticationFailed('This token has been blacklisted.')

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the token from request header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            # Check if the token is blacklisted
            check_blacklist(token)
        
        # Call the base method (standard JWT auth)
        return super().authenticate(request)
