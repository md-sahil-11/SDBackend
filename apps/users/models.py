import re
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.users.managers import UserManager


def validate_email(email: str) -> str:
    if email:
        pattern = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")  
        if not re.fullmatch(pattern, email):  
            raise ValidationError('Invalid email')

    return email


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(default="Anonymous", max_length=100, blank=True)
    email = models.EmailField(unique=True, db_index=True, validators=[validate_email])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)
    avatar = models.TextField(null=True, blank=True)

    USERNAME_FIELD = "email"

    objects = UserManager()


class ResestToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="reset_tokens", on_delete=models.CASCADE, null=True, blank=True)