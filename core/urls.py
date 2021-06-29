from django.urls import path

from core import views

urlpatterns = [
    path(
        "register/",
        views.RegistrationAPIView.as_view(),
        name="register-api",
    ),
    path(
        "jwt/login/",
        views.ObtainTokenLogin.as_view(),
        name="user-login",
    ),
]
