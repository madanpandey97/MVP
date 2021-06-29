import logging

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from general_backend import errors
from core import serializers as user_serializers
from core import utils
from core.models import User as User_model, User

logger = logging.getLogger(__name__)


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = user_serializers.UserCreateSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        data = request.data
        logger.info(f"User signup request with data {data}")
        if data.get("email"):
            data["email"] = data["email"].lower()

        if data.get("username", "email"):
            data["username"] = data["email"].lower()

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        logger.info(f"saving user info for {data}")
        user = serializer.save()

        logger.info(f"generating access token for {user}")
        tokens = utils.get_tokens_for_user(user)

        return Response(
            {"status": True, "AccessToken": tokens["access"]},
            status=status.HTTP_201_CREATED,
        )


class ObtainTokenLogin(APIView):
    def post(self, request, *args, **kwargs):
        logger.info(f"login request for {request.data}")
        if "username" not in request.data:
            logger.info(f"username not supplied")
            return Response(
                {"status": False, "username": "This field is required"},
                status=status.HTTP_200_OK,
            )
        if "password" not in request.data:
            logger.info(f"password not supplied required")
            return Response(
                {"status": False, "password": "This field is required"},
                status=status.HTTP_200_OK,
            )

        logger.info(f"looking for user")
        user = User_model.objects.filter(username=request.data["username"]).first()
        if not user:
            logger.info(f"{user} not found")
            return Response(
                {"status": False, "user": "This field is required"},
                status=status.HTTP_200_OK,
            )

        credentials = {
            "username": request.data["username"],
            "password": request.data["password"],
        }

        user = authenticate(**credentials)
        if user:
            logger.info(f"{user} generating access tokens")
            tokens = utils.get_tokens_for_user(user)

            return Response(
                {
                    "message": "You have successfully Logged In",
                    "status": True,
                    "AccessToken": tokens["access"],
                },
                status=status.HTTP_200_OK,
            )
        else:
            logger.info(f"wrong credentials supplied")
            return Response(
                {
                    "message": "email or password does not match, please enter correct details",
                    "status": False,
                },
                status=status.HTTP_200_OK,
            )
