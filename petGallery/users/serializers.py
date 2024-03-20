from rest_framework import serializers
from users.models import CustomUser, Account, SecurityQuestion
import django.contrib.auth.password_validation as validators


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "bio", "age", "gender", "animal", "breed"]


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "bio", "age", "gender", "animal", "breed", "user"]


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    account = AccountCreateSerializer()

    class Meta:
        model = CustomUser
        fields = ["username", "password", "confirm_password", "account"]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        account = validated_data.pop("account")
        user = CustomUser.objects.create_user(username=username, password=password)
        Account.objects.create(user=user, **account)
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "date_joined", "last_login", "is_active"]


class AccountInfoSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()

    class Meta:
        model = Account
        fields = "__all__"


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "name",
            "bio",
            "age",
            "gender",
            "animal",
            "breed",
        ]


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validators.validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("old_password", "new_password", "confirm_password")

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class SecurityQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityQuestion
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": False},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        security_question = SecurityQuestion.objects.create(user=user, **validated_data)
        return security_question
