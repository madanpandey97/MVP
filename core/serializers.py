import re

from django.db import transaction
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import serializers

from general_backend import errors
from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    phone = PhoneNumberField(null=True, blank=True)
    fullname = serializers.CharField(required=True)
    source = serializers.CharField(required=False)

    def validate(self, attrs):
        if not attrs.get("password") == attrs.pop("confirm_password"):
            raise serializers.ValidationError(errors.UR_PASS_AND_CONFRM_PASS_DONT_MATCH)

        # username = attrs.get("username", '')
        # if not re.match(r"^[a-zA-Z0-9\-\_.]*$", username):
        #     raise serializers.ValidationError(errors.USER_NAME_NOT_ALLOWED)

        if attrs.get("phone"):
            if User.objects.filter(phone=attrs.get("phone")).exists():
                raise serializers.ValidationError(errors.PHONE_NUM_ALREADY_REGISTERED)
        else:
            raise serializers.ValidationError("Phone number required")

        if attrs.get("email"):
            if User.objects.filter(email=attrs.get("email")).exists():
                raise serializers.ValidationError(
                    errors.THE_EMAIL_IS_ALREADY_REGISTERED
                )
        else:
            raise serializers.ValidationError(errors.EMAIL_REQUIRED)

        return attrs

    @transaction.atomic()
    def create(self, validated_data):

        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.is_active = True
        user.is_superuser = False
        user.save()

        return user

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "fullname",
            "source",
            "phone",
            "password",
            "confirm_password",
        )


class ProfileSerializer(serializers.ModelSerializer):
    """
    return user's profile
    """

    class Meta:
        model = User
        exclude = (
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "jwt_access_token",
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    User profile update serializer
    """

    class Meta:
        model = User
        fields = ["fullname", "bio", "timezone", "location"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    validate password, confirm_password and save new password for the user
    """

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    old_password = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True
    )

    class Meta:
        model = User
        fields = ("password", "confirm_password", "old_password")


class ForgotPasswordUserNameOTPSerializer(serializers.ModelSerializer):
    """
    checking given username in User modal
    """

    class Meta:
        model = User
        fields = ("email",)


class ForgotPasswordVerifyOTPSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password", "code")

    def validate(self, attrs):
        if not attrs.get("password") == attrs.pop("confirm_password"):
            raise serializers.ValidationError(errors.UR_PASS_AND_CONFRM_PASS_DONT_MATCH)
        return attrs
