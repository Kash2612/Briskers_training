
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import generics, permissions, status
from .models import Post, Profile, BlacklistedToken
from .serializers import PostSerializer, SignupSerializer, LoginSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.decorators.csrf import csrf_exempt



# List and Create posts
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Optional: Add pagination if needed

    def perform_create(self, serializer):
        # Associate the author with the post
        serializer.save(author=self.request.user)


# List posts by a specific user
class UserPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # Optional: Add pagination if needed

    def get_queryset(self):
        # Filter posts by the username provided in the URL
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=user).order_by('-date_posted')


# Retrieve a single post
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


# Update a post (restricted to the author)
class PostUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Ensure the author cannot be changed
        if serializer.instance.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to edit this post.")
        serializer.save()


# Delete a post (restricted to the author)
class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise ValueError("You do not have permission to delete this post.")
        instance.delete()

class UserRegisterView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        data = request.data
        serializer = SignupSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()  # Save the new user to the database
            user_serializer = UserSerializer(user)  # Serialize the user for response
            return Response({
                "status": True,
                "message": "User created successfully",
                "data": user_serializer.data  # Include serialized user data in response
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

# FOR AUTH TOKEN

# class UserLoginView(APIView):
#     permission_classes = [AllowAny]

#     @csrf_exempt
#     def post(self, request):
#         data = request.data
#         serializer = LoginSerializer(data=data)

#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']

#             user = authenticate(username=username, password=password)

#             if user is not None:
#                 # Generate the token
#                 token, created = Token.objects.get_or_create(user=user)
#                 return Response({
#                     "status": True,
#                     "data": {"token": token.key}
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({
#                     "status": False,
#                     "message": "Invalid credentials"
#                 }, status=status.HTTP_401_UNAUTHORIZED)

#         return Response({
#             "status": False,
#             "message": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         # Get the user's token
#         token = Token.objects.get(user=request.user)
        
#         # Delete the token to invalidate it
#         token.delete()
        
#         return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


# for JWT Token 
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None:  # If the user exists and the credentials are valid
                # Create a JWT token using the RefreshToken
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "status": True,
                    "data": {
                        "access_token": access_token,
                        "refresh_token": str(refresh)
                    }
                }, status=200)
            else:
                return Response({
                    "status": False,
                    "message": "Invalid credentials"
                }, status=401)

        return Response({
            "status": False,
            "message": serializer.errors
        }, status=400)

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             # Get the refresh token from the request data
#             refresh_token = request.data["refresh"]
#             # Create a token object
#             token = RefreshToken(refresh_token)
#             # Blacklist the token
#             token.blacklist()
            
#             return Response({"message": "Successfully logged out"}, status=205)
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract token from Authorization header
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                
                # Create AccessToken object to verify and decode the token
                access_token = AccessToken(token)
                
                # Add token to the blacklist
                BlacklistedToken.objects.create(token=token)
                
                # Return a success message
                return Response({"message": "Successfully logged out, and token has been blacklisted."}, status=200)
            else:
                return Response({"detail": "Authorization header missing or malformed."}, status=400)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)


# Detail view for an author (e.g., their profile)
# class AuthorDetailView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = PostSerializer
#     lookup_field = 'username'
#     permission_classes = [permissions.AllowAny]


# @login_required
# def about(request):
#     return render(request, 'blog/about.html', {'title': 'About'})


