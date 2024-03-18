from rest_framework import serializers
from users.models import CustomUser, Account


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "bio", "age", "gender", "animal", "breed"]


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


class UserLoginSerilaizer(serializers.Serializer):

    class Meta:
        model = CustomUser
        fields = ["username", "password"]

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = CustomUser.objects.filter(username=username).first()
            if user and user.check_password(password):
                return attrs
            else:
                raise serializers.ValidationError("Invalid username or password")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'")
