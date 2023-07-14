from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from apps.users.api.serializers import UserSerializer
from apps.users.models import ResestToken, User
from apps.users.services import *
from shared.notify import notify
from shared.choices import NotifyActionType


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_guest=False)
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.AllowAny,),
    )
    def login(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        
        user = login_user_service(email, password)
        if user is None:
            return Response({"success": False, "err": "Invalid password or email!"}, status=status.HTTP_404_NOT_FOUND)
        data = self.serializer_class(user).data
        data = add_token_to_user_serializer_selector(data, user)
        return Response({"success": True, 
            "data": data
        }, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def logout(self, request, *args, **kwargs):
        logout_user_service(request.user)
        return Response({"success": True}, status=status.HTTP_200_OK)
    
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.AllowAny,),
    )
    def register(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        name = request.data.get("name")
        user = register_user_service(email, password, name)
        if not user:
            return Response({"success": False, "err": "Invalid password or email!"})
        data = self.serializer_class(user).data
        data = add_token_to_user_serializer_selector(data, user)
        
        # verification email send
        notify(user=user, subject="Verify your email", mail_template=NotifyActionType.VERIFICATION.value)
        
        return Response({"success": True, 
            "data": data
        }, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["PUT"],
        permission_classes=(permissions.IsAuthenticated,),
        url_path="verify-email"
    )
    def verify_email(self, request, *args, **kwargs):
        request.user.is_email_verified = True
        request.user.save()
        return Response({"success": True}, status=status.HTTP_200_OK)
    
    @action(
        detail=False,
        methods=["PUT"],
        permission_classes=(permissions.AllowAny,),
        url_path="reset-password"
    )
    def reset_password(self, request, *args, **kwargs):
        password1 = request.data.get("password1")
        password2 = request.data.get("password2")
        token = request.data.get("token")
        if password1 != password2:
            raise ValidationError("Password not matching!")
        
        reset_token = get_object_or_404(ResestToken, id=token)
        user = reset_token.user
        reset_token.delete()
        user.set_password(password1)
        user.save()
        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.AllowAny,),
        url_path="reset-password-email"
    )
    def send_reset_password_email(self, request, *args, **kwargs):
        email = request.data.get("email")
        user = get_object_or_404(User, email=email)
        token, _ = ResestToken.objects.get_or_create(user=user)
        notify(
            user=user, 
            subject="Reset your password", 
            mail_template=NotifyActionType.RESET_PASSWORD.value,
            token=token.id
        )
        return Response({"success": True}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=(permissions.IsAuthenticated,),
        url_path="get-user"
    )
    def get_user(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        data = serializer.data
        data = add_token_to_user_serializer_selector(data, request.user)
        
        return Response(data, status=status.HTTP_200_OK)