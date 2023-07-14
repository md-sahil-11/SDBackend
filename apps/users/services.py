import re

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from rest_framework.authtoken.models import Token

from apps.users.models import User
from shared.create_avatar import create_avatar
from shared.random_generator import get_random_animal_name, get_random_string


def login_user_service(email: str, password: str) -> User:
    user = authenticate(email=email.lower(), password=password)
    return user
    

def register_user_service(email: str, password: str, name: str) -> User:
    user = User.objects.create(email=email, name=name)
    user.avatar = create_avatar(name)
    user.set_password(password)
    user.save()
    
    return user


def create_guest_user() -> User:
    name = get_random_animal_name()
    password = str(hash(name))
    email = f"{name}/{get_random_string(8)}@guestemail.com"
    name = f"Anonymous {name}"
    user = register_user_service(email, password, name)
    user.is_guest = True
    user.save()

    return user


def logout_user_service(user: User) -> None:
    Token.objects.filter(user=user).delete()


def add_token_to_user_serializer_selector(data: any, user: User) -> any:
    token, _ = Token.objects.get_or_create(user=user)
    data['token'] = token.key
    return data