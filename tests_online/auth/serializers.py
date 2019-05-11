from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', model.USERNAME_FIELD, model.EMAIL_FIELD)


class SignUpSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        User = get_user_model()
        return User.objects.create_user(**validated_data)

    class Meta:
        model = get_user_model()
        fields = ('id', model.USERNAME_FIELD, model.EMAIL_FIELD, 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
