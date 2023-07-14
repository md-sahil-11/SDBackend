from django.conf import settings

from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "image",
            "created_at",
            "is_guest",
            "is_email_verified"
        )
        read_only_fields = (
            "created_at",
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["image"] is None:
            data["image"] = instance.avatar

        return data
    
    