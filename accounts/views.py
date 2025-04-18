from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserSerializer, LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView

User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    """View for user registration that also returns an auth token"""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate or get auth token
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully!"
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """Custom login view that returns user details with token"""
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({
                'error': 'Invalid username or password'
            }, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveUpdateAPIView):
    """View for retrieving and updating user details"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """View for logging out a user by deleting their auth token"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Simply delete the token to force a login
        request.user.auth_token.delete()
        return Response({
            "message": "Successfully logged out."
        }, status=status.HTTP_200_OK)