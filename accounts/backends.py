from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Q
from django.http.request import HttpRequest

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, username: str | None = None, password: str | None = None, **kwargs: Any) -> AbstractBaseUser | None:
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            return None  # Return None if user is not found
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
