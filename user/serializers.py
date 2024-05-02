from tokenize import TokenError
from django.contrib import auth
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import phone_number_regex, User, UserProfile
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
        )
        read_only_fields = ('email', 'phone_number')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'user',
            'photo',
            'address'
        )

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        email = self.data['user']['email']
        phone_number = self.data['user']['phone_number']
        user = User.objects.get(email=email, phone_number=phone_number)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.update(user, user_data)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance


