from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
# No need for extra email validator imports if using EmailField

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration with password validation"""
    email = serializers.EmailField(required=True) # Explicitly declaration of email as EmailField for automatic format validation
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label="Confirm Password") # Added the label better representation in browsable APIs or forms

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'date_of_birth')
        # extra_kwargs for email is not strictly needed now as EmailField handles requirement,
        # but keeping it doesn't hurt and makes the requirement explicit.
        extra_kwargs = {'email': {'required': True}}

    def validate_passwords(self, attrs):
        """Validate that both password fields match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate(self, attrs):
        # Email format is handled by the EmailField automatically before this step.
        attrs = self.validate_passwords(attrs)
        # Check if username and email are different
        if 'username' in attrs and 'email' in attrs and attrs['username'] == attrs['email']:
            raise serializers.ValidationError("Username and email cannot be the same.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login credentials"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_of_birth')
        read_only_fields = ('id',)