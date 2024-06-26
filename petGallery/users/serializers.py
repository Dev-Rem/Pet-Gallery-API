from rest_framework import serializers
from users.models import (
    CustomUser,
    Account,
    SecurityQuestion,
    FollowAccount,
    BlockAccount,
    FollowRequest,
)
import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.dispatch import Signal

# Define a signal
my_signal = Signal()


class InActiveUser(AuthenticationFailed):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "User is not active, please confirm your email"
    default_code = "user_is_inactive"


# noinspection PyAbstractClass
class CustomTokenObtainPairSerializer(TokenObtainSerializer):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_active:
            raise InActiveUser()

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "bio", "age", "gender", "animal", "breed"]


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "bio", "age", "gender", "animal", "breed", "private", "user"]


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
        my_signal.send(sender=CustomUser)
        Account.objects.create(user=user, **account)
        return user


class FollowAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowAccount
        fields = "__all__"


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "date_joined",
            "last_login",
            "is_active",
        ]


class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowAccount
        fields = ["following_id", "created_at", "updated_at"]


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowAccount
        fields = ["follower_id", "created_at", "updated_at"]


class AccountInfoSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "bio",
            "age",
            "gender",
            "animal",
            "breed",
            "private",
            "user",
            "followers",
            "following",
            "created_at",
            "updated_at",
        ]

    def get_following(self, obj):
        following_ids = FollowAccount.objects.filter(follower=obj).values_list(
            "following_id", flat=True
        )
        return following_ids.count()

    def get_followers(self, obj):
        followers_ids = FollowAccount.objects.filter(following=obj).values_list(
            "follower_id", flat=True
        )
        return followers_ids.count()


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
        fields = ["old_password", "new_password", "confirm_password"]

    def validate(self, attrs):
        # Check if the new password is the same as the current password
        user = self.context["request"].user
        if check_password(attrs["new_password"], user.password):
            raise serializers.ValidationError(
                {"new_password": "New password cannot be the same as the old password."}
            )

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Old and new password does not match."}
            )
        self.validate_old_password(attrs["old_password"])
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value


class ResetPasswordSerialzer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validators.validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)
    security_answer = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["new_password", "confirm_password", "security_answer"]

    def validate(self, attrs):
        # Check if the new password and confirm password match
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        # Check if the new password is the same as the current password
        user = self.context["request"].user
        if check_password(attrs["new_password"], user.password):
            raise serializers.ValidationError(
                {"new_password": "New password cannot be the same as the old password."}
            )

        # Validate the security answer
        self.validate_security_answer(attrs["security_answer"])

        return attrs

    def validate_security_answer(self, value):
        user = self.context["request"].user
        try:
            security_question = SecurityQuestion.objects.get(user=user)
        except SecurityQuestion.DoesNotExist:
            raise serializers.ValidationError(
                {"security_question": "Security question not set for the user"}
            )

        if value != security_question.answer:
            raise serializers.ValidationError(
                {"security_answer": "Security answer is not correct"}
            )

        return value


class SecurityQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityQuestion
        fields = "__all__"
        lookup_field = "user.username"
        extra_kwargs = {
            "user": {"required": False},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        security_question = SecurityQuestion.objects.create(user=user, **validated_data)
        return security_question


class BlockAccountSerializer(serializers.ModelSerializer):
    users = AccountInfoSerializer(many=True)

    class Meta:
        model = BlockAccount
        fields = "__all__"


class FollowRequestListSerializer(serializers.ModelSerializer):
    request_to = AccountInfoSerializer()
    request_from = AccountInfoSerializer()

    class Meta:
        model = FollowRequest
        fields = ["request_from", "request_to", "status", "created_at", "updated_at"]


class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = ["request_from", "request_to", "status", "created_at", "updated_at"]
