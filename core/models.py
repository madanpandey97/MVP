from datetime import datetime

import pytz
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = f"{self.model.USERNAME_FIELD}__exact"
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, username, email=None, fullname=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(
            username=username, email=self.normalize_email(email), fullname=fullname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_staffuser(
            username=username,
            email=email,
            password=password,
        )
        user.email = email
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.role = "admin"
        user.save(using=self._db)
        return user


class User(TimeStampModel, AbstractBaseUser):
    email = models.EmailField(null=True, blank=True, unique=True, db_index=True)
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    objects = UserManager()

    def __str__(self):
        # return self.full_name
        return f"{self.username}-------{self.fullname}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class UserFollower(TimeStampModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="friends")
    followers = models.ManyToManyField(User)
