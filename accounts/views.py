from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model

from .serializers import UserRegistrationSerializer, UserSerializer, LoginSerializer

User = get_user_model()

class TokenResponseMixin:
    """Mixin for consistent token-based responses"""
    def get_token_response(self, user):
        """Generate token and return consistent response format"""
        token, _ = Token.objects.get_or_create(user=user)
        return {
            "token": token.key,
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        }


class RegisterUserView(TokenResponseMixin, generics.CreateAPIView):
    """API endpoint for user registration"""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = self.get_token_response(user)
        response_data["message"] = "User created successfully!"

        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(TokenResponseMixin, generics.GenericAPIView):
    """API endpoint for user login"""
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(self.get_token_response(user), status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveUpdateAPIView):
    """API endpoint for retrieving and updating the authenticated user's details"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """API endpoint for user logout"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"message": "Successfully logged out."},
            status=status.HTTP_200_OK
        )