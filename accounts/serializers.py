from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Public representation of a user, without administrative or secret fields."""

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'tel', 'photo', 'sexe',
            'date_joined',
        )
        read_only_fields = ('id', 'date_joined')


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'tel', 'photo', 'sexe')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'tel': {'required': False, 'allow_null': True, 'allow_blank': True},
            'photo': {'required': False, 'allow_null': True},
            'sexe': {'required': False, 'allow_null': True},
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        return User.objects.create_user(password=password, **validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            email=attrs['email'],
            password=attrs['password'],
        )
        if user is None:
            raise serializers.ValidationError(
                {'detail': 'Adresse e-mail ou mot de passe incorrect.'}
            )
        if not user.is_active:
            raise serializers.ValidationError({'detail': 'Ce compte est désactivé.'})

        attrs['user'] = user
        return attrs
