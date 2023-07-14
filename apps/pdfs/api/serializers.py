from rest_framework import serializers

from apps.pdfs.models import CommentLike, CommentReply, Pdf, PdfMember, Comment
from apps.users.api.serializers import UserSerializer
from apps.users.models import User


class PdfSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    creator = UserSerializer(source="created_by", read_only=True)
    members = serializers.SerializerMethodField(read_only=True)
    sharable_link = serializers.SerializerMethodField(read_only=True)
    cover_image = serializers.ImageField(required=False)
    
    class Meta:
        model = Pdf
        fields = (
            "id",
            "title",
            "file",
            "cover_image",
            "description",
            "created_by",
            "creator",
            "pages",
            "size",
            "members",
            "sharable_link"
        )

    def get_members(self, instance):
        members = instance.members.all()
        member_ids = list(members[:3].values_list("user_id", flat=True))
        users = User.objects.filter(id__in=member_ids)
        return {
            "count": len(members),
            "members": UserSerializer(users, many=True).data
        }

    def get_sharable_link(self, instance):
        return f"/d/{instance.sharable_code}"


class PdfMemberSerializer(serializers.ModelSerializer):
    pdf_id = serializers.PrimaryKeyRelatedField(
        source="pdf",
        queryset=Pdf.objects.all(), 
        write_only=True, 
        required=True
    )
    pdf = PdfSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(), 
        write_only=True, 
        required=True
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = PdfMember
        fields = (
            "id",
            "pdf_id",
            "pdf",
            "user_id",
            "user",
            "is_creator"
        )


class CommentReplySerializer(serializers.ModelSerializer):
    comment_id = serializers.PrimaryKeyRelatedField(
        source="comment",
        queryset=Comment.objects.all(), 
        write_only=True, 
        required=True
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_by = UserSerializer(source="user", read_only=True)
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = CommentReply
        fields = (
            "id",
            "text",
            "comment_id",
            "user",
            "created_by",
            "is_liked",
            "likes_count"
        )

    def get_likes_count(self, instance):
        return CommentLike.objects.filter(text_id=instance.id).count()

    def get_is_liked(self, instance):
        if (
            self.context.get("request")
            and self.context["request"].user
            and not self.context["request"].user.is_anonymous
        ):
            return CommentLike.objects.filter(
                user=self.context["request"].user, text_id=instance.id
            ).exists()

        return False
        

class CommentSerializer(serializers.ModelSerializer):
    pdf_id = serializers.PrimaryKeyRelatedField(
        source="pdf",
        queryset=Pdf.objects.all(), 
        write_only=True, 
        required=True
    )
    pdf = PdfSerializer(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_by = UserSerializer(source="user", read_only=True)
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    replies = CommentReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "user",
            "pdf",
            "created_by",
            "pdf_id",
            "is_liked",
            "likes_count",
            "replies"
        )

    def get_likes_count(self, instance):
        return CommentLike.objects.filter(text_id=instance.id).count()

    def get_is_liked(self, instance):
        if (
            self.context.get("request")
            and self.context["request"].user
            and not self.context["request"].user.is_anonymous
        ):
            return CommentLike.objects.filter(
                user=self.context["request"].user, text_id=instance.id
            ).exists()

        return False


class CommentDetailSerializer(serializers.ModelSerializer):
    pdf_id = serializers.PrimaryKeyRelatedField(
        source="pdf",
        queryset=Pdf.objects.all(), 
        write_only=True, 
        required=True
    )
    pdf = PdfSerializer(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_by = UserSerializer(source="user", read_only=True)
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    replies = CommentReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "user",
            "pdf",
            "created_by",
            "pdf_id",
            "is_liked",
            "likes_count",
            "replies"
        )

    def get_likes_count(self, instance):
        return CommentLike.objects.filter(text_id=instance.id).count()

    def get_is_liked(self, instance):
        if (
            self.context.get("request")
            and self.context["request"].user
            and not self.context["request"].user.is_anonymous
        ):
            return CommentLike.objects.filter(
                user=self.context["request"].user, text_id=instance.id
            ).exists()

        return False