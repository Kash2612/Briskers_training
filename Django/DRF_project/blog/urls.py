from django.urls import path

from .views import (
    PostListCreateView,
    UserPostListView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    UserRegisterView,
    UserLoginView,
    TokenObtainPairView,
    TokenRefreshView,
    LogoutView
)

urlpatterns = [
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/user/<str:username>/posts/', UserPostListView.as_view(), name='user-post-list'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('api/posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('api/posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # path('api/user/<str:username>/', AuthorDetailView.as_view(), name='author-detail'),

    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),

    # Add JWT Token Obtain and Refresh views here
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('logout/', LogoutView.as_view(), name='logout')


]