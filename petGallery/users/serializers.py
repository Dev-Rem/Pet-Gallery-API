from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import Account
from django.contrib.auth.hashers import make_password


class AccountRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = [
            "name",
            "username",
            "bio",
            "age",
            "gender",
            "animal",
            "breed",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")  # Remove password from validated data
        validated_data["password"] = make_password(password)  # Hash password
        account = Account.objects.create(**validated_data)
        return account


class UserLoginSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = []


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "name",
            "username",
            "age",
            "gender",
            "animal",
            "breed",
        ]
