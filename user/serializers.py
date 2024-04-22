from tokenize import TokenError

from django.contrib import auth
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import phone_number_regex, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        token = self.get_token(self.user)
        print(token)
        data['user'] = str(self.user)
        data['token'] = str(token)
        return data


# class UserSignSerializer(serializers.Serializer):
#     phone_number = serializers.CharField(
#         required=True,
#         allow_null=False,
#         validators=[phone_number_regex,]
#     )


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     min_length=6, max_length=100)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'gender',
            'password',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number', "")
        email = attrs.get('email', "")
        gender = attrs.get('gender', "")
        if not email:
            raise serializers.ValidationError("Email should not be blank!"
                                              )
        return attrs


class LoginUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, max_length=50)
    email = serializers.EmailField(min_length=6, max_length=50)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.get_pair_token()['refresh'],
            'access': user.get_pair_token()['access'],
        }

    class Meta:
        model = User
        fields = (
            'password',
            'email',
            'tokens',
        )

    def validate(self, attrs):
        email = attrs.get('email', "")
        password = attrs.get('password', "")
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Email and/or password is incorrect!")
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive!")
        return {
            'email': user.email,
            'tokens': user.get_pair_token,
        }


class LogoutUserSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get('refresh', "")
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("Invalid token!")
