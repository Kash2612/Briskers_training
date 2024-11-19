from django.contrib import admin
from .models import Post, BlacklistedToken

admin.site.register(Post)
admin.site.register(BlacklistedToken)